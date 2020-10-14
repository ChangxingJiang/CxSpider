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

from Selenium4R import Chrome
from selenium.common.exceptions import NoSuchElementException

from toolkit import file


def crawler():
    browser = Chrome(cache_path=r"E:\temp")

    account_list = file.load_as_string("huya_account_list.txt")
    for account_url in account_list.split("\n"):
        browser.get(account_url)

        # 读取直播间订阅数量
        text_subscribe = ""
        try:
            label_subscribe = browser.find_element_by_xpath('//*[@id="activityCount"]')
            if label_subscribe is not None:
                text_subscribe = label_subscribe.text
        except NoSuchElementException:
            pass

        # 读取直播间ID
        text_id = ""
        try:
            label_id = browser.find_element_by_css_selector(
                '#J_roomHeader > div.room-hd-l > div.host-info > div.host-detail.J_roomHdDetail > span.host-rid')
            if label_id is not None:
                text_id = label_id.text
        except NoSuchElementException:
            pass

        print(account_url, text_id, text_subscribe)

        time.sleep(3)


if __name__ == "__main__":
    crawler()
