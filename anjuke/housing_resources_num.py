"""
安居客各地房源数量爬虫

需要第三方模块：
BeautifulSoup4 >= 4.9.0
Selenium4R >= 0.0.3
Utils4R >= 0.0.2

函数说明：
crawler_city_list : 采集城市编码列表
crawler_city_resources : 采集城市房源数量

@author: 长行
@version: 1.1
@create: 2019.12.17
@revise: 2020.06.09
"""

import time

import Utils4R as Utils
from Selenium4R import Chrome
from bs4 import BeautifulSoup


def crawler_city_list():
    """
    采集城市编码列表
    """
    browser = Chrome(cache_path=r"E:\Temp")
    browser.get("https://www.anjuke.com/sy-city.html")

    bs = BeautifulSoup(browser.page_source, "lxml")  # 将网页转化为BeautifulSoup结构
    city_dict = dict()
    for city_label in bs.select("body > div.content > div > div.letter_city > ul > li > div > a"):
        city_name = city_label.get_text()
        city_code = city_label["href"].replace("https://", "").replace(".anjuke.com", "")
        city_dict[city_name] = city_code
        print(city_name, city_code)

    Utils.io.write_json("anjuke_city_code.json", city_dict)
    browser.quit()


def crawler_city_resources():
    """
    采集城市房源数量
    """
    cities = Utils.io.load_json("anjuke_city_code.json")
    city_info = Utils.io.load_json("anjuke_city_infor.json")

    browser = Chrome(cache_path=r"E:\Temp")
    for city_name in cities:
        if city_name not in city_info:
            city_code = cities[city_name]
            browser.get("https://" + city_code + ".fang.anjuke.com/?from=navigation")
            bs = BeautifulSoup(browser.page_source, "lxml")  # 将网页转化为BeautifulSoup结构
            city_label = bs.select_one(
                "#container > div.list-contents > div.list-results > div.key-sort > div.sort-condi > span > em")
            if city_label is not None:
                city_num = city_label.text
            else:
                city_num = 0
                if bs.select_one("#header > div.site-search > div.sel-city > a > span") is None:
                    print("可能出现反爬虫，请处理...")
                    time.sleep(300)
                    break

            city_num = int(city_num)
            city_info[city_name] = city_num

            Utils.io.write_json("anjuke_city_infor.json", city_info)

            time.sleep(2)

    browser.quit()


if __name__ == "__main__":
    crawler_city_list()
    crawler_city_resources()
