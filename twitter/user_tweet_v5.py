"""
Twitter用户推文爬虫

需要第三方模块：
Selenium4R >= 0.0.3

@author: ChangXing
@version: 5.1
@create: 2017.12.30
@revise: 2020.07.22
"""

import copy
import datetime as dt
import re
import time
from urllib import parse

from Selenium4R import Chrome
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

SELECTOR_TEST = "main > div > div > div > div:nth-child(1) > div > div:nth-child(2) > div > div"
SELECTOR_OUTER = "main > div > div > div > div:nth-child(1) > div > div:nth-child(2) > div > div > section > div > div > div"
SELECTOR_ID = "article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(1) > a"
SELECTOR_TIME = "article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(1) > a > time"
SELECTOR_RETWEET = "article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div"
SELECTOR_CONTENT = "article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)"
SELECTOR_FEEDBACK = "article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div[role='group']"
SELECTOR_FROM_USER = "article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div > div > div > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(1) > div > div > div > div > div"
SELECTOR_FROM_CONTENT = "article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div > div > div > div:nth-child(2) > div > div:nth-child(2)"


def crawler(driver, user_name, template, since=None, until=None):
    """
    抓取Twitter用户推文
    填写数据模板中的tweet_id、time、text、replies、retweets、likes属性

    :param driver: <selenium.webdriver.chrome.webdriver.WebDriver> Chrome浏览器对象
    :param user_name: <str> Twitter用户名
    :param template: <dict> 返回值数据模板
    :param since: <datetime> 开始抓取推文的日期(包含)
    :param until: <datetime> 结束抓取推文的日期(不包含)
    :return: <list:dict> 指定Twitter用户在指定时间范围内的推文列表
    """

    tweet_list = list()

    # 生成请求的Url
    query_sentence = list()
    query_sentence.append("from:%s" % user_name)  # 搜索目标用户发布的推文
    if since is not None:
        query_sentence.append("since:%s" % str(since))  # 设置开始时间
        query_sentence.append("until:%s" % str(until))  # 设置结束时间
    query = " ".join(query_sentence)  # 计算q(query)参数的值
    params = {
        "q": query,
        "f": "live"
    }
    actual_url = "https://twitter.com/search?" + parse.urlencode(params)

    # 打开目标Url
    driver.get(actual_url)
    time.sleep(3)

    label_test = driver.find_element_by_css_selector(SELECTOR_TEST)
    if "你输入的词没有找到任何结果" in label_test.text:
        return tweet_list

    # 定位标题外层标签
    label_outer = driver.find_element_by_css_selector(SELECTOR_OUTER)
    driver.execute_script("arguments[0].id = 'outer';", label_outer)  # 设置标题外层标签的ID

    # 循环遍历外层标签
    tweet_id_list = list()
    for _ in range(1000):
        last_label_tweet = None
        for label_tweet in label_outer.find_elements_by_xpath('//*[@id="outer"]/div'):  # 定位到推文标签
            # 读取推文ID
            try:
                label_id = label_tweet.find_element_by_css_selector(SELECTOR_ID)
                tweet_id = re.search("[0-9]+$", label_id.get_attribute("href")).group()
            except NoSuchElementException:
                print("未找到推文ID标签(NoSuchElementException)")
                continue
            except StaleElementReferenceException:
                print("未找到推文ID标签(StaleElementReferenceException)")
                continue

            # 判断推文是否已被抓取(若未被抓取则解析推文)
            if tweet_id in tweet_id_list:
                continue
            else:
                tweet_id_list.append(tweet_id)
                last_label_tweet = label_tweet

                # 解析推文发布时间
                try:
                    label_time = label_tweet.find_element_by_css_selector(SELECTOR_TIME)
                    tweet_time = label_time.get_attribute("datetime").replace("T", " ").replace(".000Z", "")
                except NoSuchElementException:
                    print("未找到推文时间标签(NoSuchElementException)")
                    continue
                except StaleElementReferenceException:
                    print("未找到推文时间标签(StaleElementReferenceException)")
                    continue

                # 判断是否为转推
                tweet_replies = 0  # 推文回复数
                tweet_retweets = 0  # 推文转推数
                tweet_likes = 0  # 推文喜欢数
                tweet_from_user = None  # 原推文发布用户
                tweet_from_content = None  # 原推文内容

                # 解析推文内容
                try:
                    label_content = label_tweet.find_element_by_css_selector(SELECTOR_CONTENT)
                    tweet_content = label_content.text
                except NoSuchElementException:
                    print("未找到推文内容标签(NoSuchElementException)")
                    continue
                except StaleElementReferenceException:
                    print("未找到推文内容标签(StaleElementReferenceException)")
                    continue

                # 定位到推文反馈数据标签
                try:
                    label_feedback = label_tweet.find_element_by_css_selector(SELECTOR_FEEDBACK)
                    text_feedback = label_feedback.get_attribute("aria-label")

                    # 解析推文反馈数据
                    for feedback_item in text_feedback.split(","):
                        if "回复" in feedback_item:
                            tweet_replies = re.search("[0-9]+", feedback_item).group()
                        if "转推" in feedback_item:
                            tweet_retweets = re.search("[0-9]+", feedback_item).group()
                        if "喜欢" in feedback_item:
                            tweet_likes = re.search("[0-9]+", feedback_item).group()
                except NoSuchElementException:
                    print("未找到推文反馈数据标签(NoSuchElementException)")
                    continue
                except StaleElementReferenceException:
                    print("未找到推文反馈数据标签(StaleElementReferenceException)")
                    continue

                # 处理转推的情况
                label_retweet = label_tweet.find_elements_by_css_selector(SELECTOR_RETWEET)  # 判断是否为转推
                if len(label_retweet) >= 1:
                    # 解析转推原推文作者
                    try:
                        label_from_user = label_tweet.find_element_by_css_selector(SELECTOR_FROM_USER)
                        tweet_from_user = label_from_user.text
                    except NoSuchElementException:
                        print("不是转发推文或未找到原推文作者标签(NoSuchElementException)")
                        # continue
                    except StaleElementReferenceException:
                        print("不是转发推文或未找到原推文作者标签(StaleElementReferenceException)")
                        # continue

                    # 解析转推原推文内容
                    try:
                        label_from_content = label_tweet.find_element_by_css_selector(SELECTOR_FROM_CONTENT)
                        tweet_from_content = label_from_content.text
                    except NoSuchElementException:
                        print("不是转发推文或未找到原推文内容标签(NoSuchElementException)")
                        # continue
                    except StaleElementReferenceException:
                        print("不是转发推文或未找到原推文内容标签(StaleElementReferenceException)")
                        # continue

                tweet_info = copy.deepcopy(template)
                tweet_info["tweet_id"] = tweet_id
                tweet_info["time"] = tweet_time
                tweet_info["text"] = tweet_content
                tweet_info["replies"] = tweet_replies
                tweet_info["retweets"] = tweet_retweets
                tweet_info["likes"] = tweet_likes
                tweet_info["from_user"] = tweet_from_user
                tweet_info["from_content"] = tweet_from_content
                tweet_list.append(tweet_info)

        # 向下滚动到最下面的一条推文
        if last_label_tweet is not None:
            driver.execute_script("arguments[0].scrollIntoView();", last_label_tweet)  # 滑动到推文标签
            time.sleep(1)
        else:
            break

    return tweet_list


if __name__ == "__main__":
    selenium = Chrome()  # 打开Selenium控制的Chrome浏览器
    # tweets = crawler(selenium, "realDonaldTrump", {}, since=dt.date(2020, 7, 20), until=dt.date(2020, 7, 24))
    tweets = crawler(selenium, "appledaily_hk", {}, since=dt.date(2020, 7, 20), until=dt.date(2020, 7, 24))
    print(tweets)
