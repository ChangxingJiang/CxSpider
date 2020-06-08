"""
安居客各地房源数量爬虫
crawler_city_list : 采集城市编码列表
crawler_city_resources : 采集城市房源数量

@author: ChangXing
@version: 1.1
@create: 2019.12.17
@revise: 2020.06.09
"""

import time

from bs4 import BeautifulSoup

import toolkit as tool


def crawler_city_list():
    """
    采集城市编码列表
    """
    browser = tool.open_chrome(use_user_dir=False)
    browser.get("https://www.anjuke.com/sy-city.html")

    bs = BeautifulSoup(browser.page_source, 'lxml')  # 将网页转化为BeautifulSoup结构
    city_dict = dict()
    for city_label in bs.select("body > div.content > div > div.letter_city > ul > li > div > a"):
        city_name = city_label.get_text()
        city_code = city_label["href"].replace("https://", "").replace(".anjuke.com", "")
        city_dict[city_name] = city_code
        print(city_name, city_code)

    tool.file.write_json("anjuke_city_code.json", city_dict)


def crawler_city_resources():
    """
    采集城市房源数量
    """
    cities = tool.file.load_as_json("anjuke_city_code.json")
    city_infor = tool.file.load_as_json("anjuke_city_infor.json")

    browser = tool.open_chrome(use_user_dir=False)
    for city_name in cities:
        if city_name not in city_infor:
            city_code = cities[city_name]
            browser.get("https://" + city_code + ".fang.anjuke.com/?from=navigation")
            bs = BeautifulSoup(browser.page_source, 'lxml')  # 将网页转化为BeautifulSoup结构
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
            city_infor[city_name] = city_num

            tool.file.write_json("anjuke_city_infor.json", city_infor)

            time.sleep(2)


if __name__ == "__main__":
    crawler_city_list()
    crawler_city_resources()
