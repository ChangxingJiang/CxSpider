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

from Selenium4R import Chrome

if __name__ == "__main__":
    browser = Chrome(cache_path=r"E:\temp")  # ChromeDriver可执行文件的路径
    browser.get("http://piaofang.maoyan.com/dashboard/web-heat")
    time.sleep(1)
    for movie_label in browser.find_elements_by_css_selector(
            "#app > div > div > div.dashboard-content > div.dashboard-list.dashboard-left.bg > div.movielist-container > div > table > tbody > tr"):
        print("排名:", movie_label.find_element_by_class_name("moviename-index").text)
        print("名称:", movie_label.find_element_by_class_name("moviename-name").text)
        print("信息:", movie_label.find_element_by_class_name("moviename-info").text)
        print("信息:", movie_label.find_element_by_class_name("heat-text").text)
        print("信息:", movie_label.find_element_by_class_name("last-col").text)
