"""
猫眼网播热度采集

需要第三方模块：
Selenium4R >= 0.0.3

@author: ChangXing
@version: 1.0
@create: 2020.05.26
@revise: -
"""

import time

import crawlertool as tool
from Selenium4R import Chrome


class SpiderMaoyanWebHeat(tool.abc.SingleSpider):
    """
    猫眼网播热度采集爬虫

    有效性检验时间:2020.12.28
    """

    def __init__(self, driver):
        self.driver = driver

    def running(self):
        driver.get("http://piaofang.maoyan.com/dashboard/web-heat")
        time.sleep(3)

        result = []

        for movie_label in driver.find_elements_by_css_selector(
                "#app > div > div > div.dashboard-content > div.dashboard-list.dashboard-left.bg > div.movielist-container > div > table > tbody > tr"):
            result.append({
                "排名": movie_label.find_element_by_class_name("moviename-index").text,
                "名称": movie_label.find_element_by_class_name("moviename-name").text,
                "信息A": movie_label.find_element_by_class_name("moviename-info").text,
                "信息B": movie_label.find_element_by_class_name("heat-text").text,
                "信息C": movie_label.find_element_by_class_name("last-col").text
            })

        return result


# ------------------- 单元测试 -------------------
if __name__ == "__main__":
    driver = Chrome(cache_path=r"E:\temp")
    print(SpiderMaoyanWebHeat(driver).running())
    driver.quit()
