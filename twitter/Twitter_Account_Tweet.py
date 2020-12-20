# coding:utf-8

"""
Twitter账号推文爬虫

@Update: 2020.10.23
"""

import re
import time
from urllib import parse

import crawlertool as tool


class SpiderTwitterTweet(tool.abc.SingleSpider):
    def __init__(self, driver):
        self.driver = driver

        # 爬虫实例的变量
        self.user_name = None

    @staticmethod
    def get_twitter_user_name(page_url: str) -> str:
        """提取Twitter的账号用户名称

        主要用于从Twitter任意账号页的Url中提取账号用户名称

        :param page_url: Twitter任意账号页的Url
        :return: Twitter账号用户名称
        """
        if pattern := re.search(r"(?<=twitter.com/)[^/]+", page_url):
            return pattern.group()

    def running(self, user_name: str, since_date, until_date):
        """执行Twitter账号推文爬虫

        :param user_name: Facebook账号主页名称（可以通过get_facebook_user_name获取）
        :param since_date: 抓取时间范围的右侧边界（最早日期）
        :param until_date: 抓取时间范围的左侧边界（最晚日期）
        :return: 推文信息列表
        """

        self.user_name = user_name

        item_list = []

        # 生成请求的Url
        query_sentence = list()
        query_sentence.append("from:%s" % user_name)  # 搜索目标用户发布的推文
        query_sentence.append("-filter:retweets")  # 过滤到所有转推的推文
        if since_date is not None:
            query_sentence.append("since:%s" % str(since_date))  # 设置开始时间
            query_sentence.append("until:%s" % str(until_date))  # 设置结束时间
        query = " ".join(query_sentence)  # 计算q(query)参数的值
        params = {
            "q": query,
            "f": "live"
        }
        actual_url = "https://twitter.com/search?" + parse.urlencode(params)
        self.console("实际请求Url:" + actual_url)

        # 打开目标Url
        self.driver.get(actual_url)
        time.sleep(3)

        # 判断是否该账号在指定时间范围内没有发文
        label_test = self.driver.find_element_by_css_selector("main > div > div > div > div:nth-child(1) > div > div:nth-child(2) > div > div")
        if "你输入的词没有找到任何结果" in label_test.text:
            return item_list

        # 定位标题外层标签
        label_outer = self.driver.find_element_by_css_selector(
            "main > div > div > div > div:nth-child(1) > div > div:nth-child(2) > div > div > section > div > div")
        self.driver.execute_script("arguments[0].id = 'outer';", label_outer)  # 设置标题外层标签的ID

        # 循环遍历外层标签
        tweet_id_set = set()
        for _ in range(1000):
            last_label_tweet = None
            for label_tweet in label_outer.find_elements_by_xpath('//*[@id="outer"]/div'):  # 定位到推文标签

                item = {}

                # 读取推文ID
                if label := label_tweet.find_element_by_css_selector(
                        "article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(1) > a"):
                    if pattern := re.search("[0-9]+$", label.get_attribute("href")):
                        item["tweet_id"] = pattern.group()
                if "tweet_id" not in item:
                    self.log("账号名称:" + user_name + "|未找到推文ID标签(第" + str(len(item_list)) + "条推文)")
                    continue

                # 判断推文是否已被抓取(若未被抓取则解析推文)
                if item["tweet_id"] in tweet_id_set:
                    continue

                tweet_id_set.add(item["tweet_id"])
                last_label_tweet = label_tweet

                # 解析推文发布时间
                if label := label_tweet.find_element_by_css_selector(
                        "article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div > div > div:nth-child(1) > a > time"):
                    item["time"] = label.get_attribute("datetime").replace("T", " ").replace(".000Z", "")

                # 解析推文内容
                if label := label_tweet.find_element_by_css_selector(
                        "article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)"):
                    item["text"] = label.text

                item["replies"] = 0  # 推文回复数
                item["retweets"] = 0  # 推文转推数
                item["likes"] = 0  # 推文喜欢数

                # 定位到推文反馈数据标签
                if label := label_tweet.find_element_by_css_selector(
                        "article > div > div > div > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div[role='group']"):
                    if text := label.get_attribute("aria-label"):
                        # 解析推文反馈数据
                        for feedback_item in text.split(","):
                            if "回复" in feedback_item:
                                if pattern := re.search("[0-9]+", feedback_item):
                                    item["replies"] = int(pattern.group())
                            if "转推" in feedback_item:
                                if pattern := re.search("[0-9]+", feedback_item):
                                    item["retweets"] = int(pattern.group())
                            if "喜欢" in feedback_item:
                                if pattern := re.search("[0-9]+", feedback_item):
                                    item["likes"] = int(pattern.group())

                item_list.append(item)

            # 向下滚动到最下面的一条推文
            if last_label_tweet is not None:
                self.driver.execute_script("arguments[0].scrollIntoView();", last_label_tweet)  # 滑动到推文标签
                self.console("执行一次向下翻页...")
                time.sleep(3)
            else:
                break

        return item_list
