"""
安居客各地房源数量爬虫

需要第三方模块：
Selenium4R >= 0.0.3
Utils4R >= 0.0.6

@Author: 长行
@Update: 2020.10.18
"""

import time

import Utils4R as Utils
from Selenium4R import Chrome


class SpiderCityCode(Utils.abc.SingleSpider):
    """采集城市编码列表"""

    def __init__(self, driver):
        self.driver = driver

    def run(self, **params):
        self.driver.get("https://www.anjuke.com/sy-city.html")

        city_dict = {}
        for city_label in self.driver.find_elements_by_css_selector("body > div.content > div > div.letter_city > ul > li > div > a"):
            city_name = city_label.text
            city_code = city_label.get_attribute("href").replace("https://", "").replace(".anjuke.com/", "")
            city_dict[city_name] = city_code

        return city_dict


class SpiderCityInfo(Utils.abc.SingleSpider):
    """采集城市房源数量"""

    def __init__(self, driver):
        self.driver = driver

    def run(self, **params):
        self.driver.get("https://" + params["city_code"] + ".fang.anjuke.com/?from=navigation")
        city_label = self.driver.find_element_by_css_selector(
            "#container > div.list-contents > div.list-results > div.key-sort > div.sort-condi > span > em")
        return int(city_label.text) if city_label else 0


def crawler():
    driver = Chrome(cache_path=r"E:\Temp")

    # 采集城市编码列表
    spider_city_code = SpiderCityCode(driver)
    result1 = spider_city_code.run()
    Utils.io.write_json("anjuke_city_code.json", result1)

    # 采集城市房源数量
    city_code_list = Utils.io.load_json("anjuke_city_code.json")
    city_info_list = Utils.io.load_json("anjuke_city_infor.json", default={})
    spider_city_info = SpiderCityInfo(driver)
    for city_name, city_code in city_code_list.items():
        if city_name not in city_info_list:
            city_info_list[city_name] = spider_city_info.run(city_code=city_code)
            Utils.io.write_json("anjuke_city_info.json", city_info_list)
            time.sleep(2)

    driver.quit()


if __name__ == "__main__":
    crawler()
