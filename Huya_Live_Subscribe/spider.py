"""
虎牙直播间订阅数爬虫
依据直播间Url列表，采集列表中直播间的订阅数(输出到控制台)
列表文件中一行一个Url

需要第三方模块：
Selenium4R >= 0.0.3

@author: ChangXing
@version: 1.2
@create: 2019.11.24
@revise: 2020.06.09
"""

import time

import crawlertool as tool
from Selenium4R import Chrome


class SpiderHuyaSubscribe(tool.abc.SingleSpider):
    def __init__(self, driver):
        self.driver = driver

    def running(self, account_url):
        self.driver.get(account_url)

        # 读取直播间订阅数量
        text_subscribe = ""
        if label_subscribe := self.driver.find_element_by_xpath('//*[@id="activityCount"]'):
            text_subscribe = label_subscribe.text

        # 读取直播间ID
        text_id = ""
        if label_id := self.driver.find_element_by_css_selector(
                '#J_roomHeader > div.room-hd-l > div.host-info > div.host-detail.J_roomHdDetail > span.host-rid'):
            text_id = label_id.text

        return text_id, text_subscribe


def crawler():
    driver = Chrome(cache_path=r"E:\temp")

    account_list = tool.io.load_string("huya_account_list.txt")

    spider = SpiderHuyaSubscribe(driver)

    for account_url in account_list.split("\n"):
        text_id, text_subscribe = spider.running(account_url)

        print(account_url, text_id, text_subscribe)

        time.sleep(3)


if __name__ == "__main__":
    crawler()
