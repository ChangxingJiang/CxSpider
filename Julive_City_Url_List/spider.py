"""
居理新房城市页面列表爬虫

需要第三方模块：
BeautifulSoup4 >= 4.9.0
Selenium4R >= 0.0.3

@author: ChangXing
@version: 1.1
@create: 2019.12.17
@revise: 2020.06.09
"""

import crawlertool as tool
from Selenium4R import Chrome
from bs4 import BeautifulSoup


class SpiderJuliveCityList(tool.abc.SingleSpider):
    def running(self):
        driver = Chrome(cache_path=r"E:\temp")
        driver.get("https://cc.julive.com/project/s")

        bs = BeautifulSoup(driver.page_source, 'lxml')  # 将网页转化为BeautifulSoup结构

        city_dict = dict()
        for element_city in bs.select(
                "body > div.container-5-2.container > div.header-v5.header-v5-2.header-normal > div > div.inn-p > div.city-position.city-tip > div.city-change-list-new > ul > li > ul > li> a"):
            city_name = element_city.text
            city_url = element_city["href"]
            city_dict[city_name] = city_url

        return city_dict


def crawler():
    spider = SpiderJuliveCityList()
    city_dict = spider.running()
    tool.io.write_json("julive_city_url_20191217.json", city_dict)


if __name__ == "__main__":
    crawler()
