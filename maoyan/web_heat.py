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
    def running(self):
        driver = Chrome(cache_path=r"E:\temp")  # ChromeDriver可执行文件的路径
        driver.get("http://piaofang.maoyan.com/dashboard/web-heat")
        time.sleep(1)

        res = []

        for movie_label in driver.find_elements_by_css_selector(
                "#app > div > div > div.dashboard-content > div.dashboard-list.dashboard-left.bg > div.movielist-container > div > table > tbody > tr"):
            res.append([
                movie_label.find_element_by_class_name("moviename-index").text,
                movie_label.find_element_by_class_name("moviename-name").text,
                movie_label.find_element_by_class_name("moviename-info").text,
                movie_label.find_element_by_class_name("heat-text").text,
                movie_label.find_element_by_class_name("last-col").text
            ])

        return res


def crawler():
    spider = SpiderMaoyanWebHeat()
    lst = spider.running()

    for elem in lst:
        print("排名:", elem[0])
        print("名称:", elem[1])
        print("信息:", elem[2])
        print("信息:", elem[3])
        print("信息:", elem[4])


if __name__ == "__main__":
    crawler()
