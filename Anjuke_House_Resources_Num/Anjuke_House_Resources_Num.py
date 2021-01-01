"""
安居客各地房源数量爬虫

需要第三方模块：
Selenium4R >= 0.0.3
Utils4R >= 0.0.6

@Author: 长行
@Update: 2020.10.18
"""

from typing import List, Dict

import crawlertool as tool
from Selenium4R import Chrome


class SpiderHouseResourcesNum(tool.abc.SingleSpider):
    """
    采集城市房源数量

    有效性检验日期 : 2020.12.28
    """

    def __init__(self, driver):
        self.driver = driver

    def running(self, city_code) -> List[Dict]:
        self.driver.get("https://{}.fang.anjuke.com/?from=navigation".format(city_code))
        city_label = self.driver.find_element_by_css_selector(
            "#container > div.list-contents > div.list-results > div.key-sort > div.sort-condi > span > em")

        return [{
            "city_code": city_code,
            "city_num": int(city_label.text) if city_label else 0
        }]


# ------------------- 单元测试 -------------------
if __name__ == "__main__":
    driver = Chrome(cache_path=r"E:\Temp")
    print(SpiderHouseResourcesNum(driver).running("anshan"))
    driver.quit()
