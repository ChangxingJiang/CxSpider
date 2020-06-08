"""
Twitter用户信息爬虫

@author: ChangXing
@version: 4.1
@create: 2020.04.23
@revise: 2020.06.08
"""

import copy
import time

from twitter_scraper import Profile

import environment as env
import toolkit as tool

XPATH_FOLLOWING_COUNT = [
    "//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div[5]/div[1]/a",
    "//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div[4]/div[1]/a"
]
XPATH_FOLLOWERS_COUNT = [
    "//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div[5]/div[2]/a",
    "//*[@id=\"react-root\"]/div/div/div/main/div/div/div/div[1]/div/div/div/div/div[1]/div/div[4]/div[2]/a"
]


def crawler_item(driver, user_name: str, template):
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
        return

    print(profile)

    for key, value in profile.items():
        template[key] = value

    # 抓取账户粉丝数和正在关注数(Selenium爬虫)
    driver.get("https://twitter.com/" + user_name)
    time.sleep(tool.get_scope_random(12))
    try:
        following_count = tool.fetch.number(driver.find_element_by_xpath(XPATH_FOLLOWING_COUNT[0]).text)
        followers_count = tool.fetch.number(driver.find_element_by_xpath(XPATH_FOLLOWERS_COUNT[0]).text)
    except:
        try:
            following_count = tool.fetch.number(driver.find_element_by_xpath(XPATH_FOLLOWING_COUNT[1]).text)
            followers_count = tool.fetch.number(driver.find_element_by_xpath(XPATH_FOLLOWERS_COUNT[1]).text)
        except:
            print("Selenium抓取关注数+正在关注失败!")
            return template

    # 依据Selenium爬虫结果修正抓取结果
    if abs(template["following_count"] - following_count) > 1000:
        print("修正正在关注数量:", template["following_count"], "→", following_count)
        template["following_count"] = following_count
    if abs(template["followers_count"] - followers_count) > 1000:
        print("修正关注者数量:", template["followers_count"], "→", followers_count)
        template["followers_count"] = followers_count

    return template


if __name__ == "__main__":
    selenium = tool.open_chrome(use_user_dir=False)  # 打开Selenium控制的Chrome浏览器
    mySQL = tool.mysql_connect("Huabang")  # 构造MySQL数据库连接对象

    if "Huabang" in env.DATA and "Media List" in env.DATA["Huabang"]:
        for media_item in env.DATA["Huabang"]["Media List"]:
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
            user_info = crawler_item(selenium, user_name=media_item[2], template=copy.deepcopy(user_template))
            record_num = mySQL.insert("twitter_user_2020_06", [user_info])
            time.sleep(tool.get_scope_random(1))
    else:
        print("榜单媒体名录不存在")
