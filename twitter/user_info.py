"""
Twitter用户信息爬虫

@author: ChangXing
@version: 4.1
@create: 2017.12.25
@revise: 2020.06.08
"""

import copy
import time

from twitter_scraper import Profile

import environment as env
import toolkit as tool
from toolkit.textCleaner import TextCleaner

XPATH_FOLLOWING_COUNT = [
    "//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div[5]/div[1]/a",
    "//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div[4]/div[1]/a"
]
XPATH_FOLLOWERS_COUNT = [
    "//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div[5]/div[2]/a",
    "//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div[4]/div[2]/a"
]


def crawler(driver, user_name: str, template):
    """
    抓取Twitter用户信息
    填写数据模板中的name、username、birthday、biography、website、profile_photo、likes_count、tweets_count、followers_count、following_count属性

    :param driver: <selenium.webdriver.chrome.webdriver.WebDriver> Chrome浏览器对象
    :param user_name: <str> Twitter用户名
    :param template: <dict> 返回值数据模板
    :return: <dict> 填写抓取数据的数据模板
    """
    # 使用twitter-scraper包抓取账户信息(关注数+正在关注数可能错误)
    try:
        profile = Profile(user_name).to_dict()
    except:
        print("账号不存在!")
        return None

    print(profile)

    for key, value in profile.items():
        template[key] = value

    # 抓取账户粉丝数和正在关注数(Selenium爬虫)
    driver.get("https://twitter.com/" + user_name)
    time.sleep(tool.get_scope_random(12))
    try:
        following_count = TextCleaner(driver.find_element_by_xpath(XPATH_FOLLOWING_COUNT[0]).text).fetch_number()
        followers_count = TextCleaner(driver.find_element_by_xpath(XPATH_FOLLOWERS_COUNT[0]).text).fetch_number()
    except:
        try:
            following_count = TextCleaner(driver.find_element_by_xpath(XPATH_FOLLOWING_COUNT[1]).text).fetch_number()
            followers_count = TextCleaner(driver.find_element_by_xpath(XPATH_FOLLOWERS_COUNT[1]).text).fetch_number()
        except:
            print("Selenium抓取关注数+正在关注失败!")
            return template

    # 依据Selenium爬虫结果修正抓取结果
    try:
        if "following_count" not in template or template["following_count"] is None:
            template["following_count"] = 0
        if "followers_count" not in template or template["followers_count"] is None:
            template["followers_count"] = 0
        if abs(template["following_count"] - following_count) > 1000 \
                or (abs(template["following_count"] - following_count) > 0 and template["following_count"] < 10000):
            print("修正正在关注数量:", template["following_count"], "→", following_count)
            template["following_count"] = following_count
        if abs(template["followers_count"] - followers_count) > 1000 \
                or (abs(template["followers_count"] - followers_count) > 0 and template["followers_count"] < 10000):
            print("修正关注者数量:", template["followers_count"], "→", followers_count)
            template["followers_count"] = followers_count
    except TypeError:
        print("修改正在关注、关注者数量失败，最终取值：正在关注 =", template["following_count"], "、关注数 =", template["followers_count"])

    return template


if __name__ == "__main__":
    selenium = tool.open_chrome(use_user_dir=False)  # 打开Selenium控制的Chrome浏览器
    mySQL = tool.mysql_connect("Huabang")  # 构造MySQL数据库连接对象

    if "Huabang" in env.DATA and "Media List" in env.DATA["Huabang"]:
        for media_item in env.DATA["Huabang"]["Media List"]:
            # if media_item[0] < 133:
            #     continue
            print("开始抓取媒体:", media_item[1], "(", media_item[0], ")", "-", media_item[3], "(", media_item[2], ")")
            user_template = {
                "media_id": media_item[0],
                "media_name": media_item[1],
                "name": None,
                "username": None,
                "birthday": None,
                "biography": None,
                "website": None,
                "profile_photo": None,
                "likes_count": None,
                "tweets_count": None,
                "followers_count": None,
                "following_count": None,
            }
            user_info = crawler(selenium, user_name=media_item[2], template=copy.deepcopy(user_template))
            if user_info is not None:
                record_num = mySQL.insert("twitter_user_2020_07", [user_info])
            time.sleep(tool.get_scope_random(1))
    else:
        print("榜单媒体名录不存在")
