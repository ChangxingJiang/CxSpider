"""
居理新房城市页面列表爬虫

@author: ChangXing
@version: 1.1
@create: 2019.12.17
@revise: 2020.06.09
"""

import crawlertool as tool
from Selenium4R import Chrome
from bs4 import BeautifulSoup


class SpiderJuliveCityUrlList(tool.abc.SingleSpider):
    """
    居理新房城市页面列表爬虫
    """

    def __init__(self, driver):
        self.driver = driver

    def running(self):
        driver.get("https://www.julive.com/project/s")

        bs = BeautifulSoup(driver.page_source, "lxml")

        result = []
        for element_city in bs.select(
                "body > div.container-5-2.container > div.header-v5.header-v5-2.header-normal > div > div.inn-p > div.city-position.city-tip > div.city-change-list-new > ul > li > ul > li> a"):
            result.append({
                "city_name": element_city.text,
                "city_url": element_city["href"]
            })

        return result


# ------------------- 单元测试 -------------------
if __name__ == "__main__":
    driver = Chrome(cache_path=r"E:\temp")
    print(SpiderJuliveCityUrlList(driver).running())
    driver.quit()
