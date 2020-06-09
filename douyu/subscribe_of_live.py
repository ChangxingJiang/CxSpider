"""
斗鱼直播间订阅数爬虫
依据直播间Url列表，采集列表中直播间的订阅数(输出到控制台)
列表文件中一行一个Url
（暂停使用：斗鱼增加字符集加密，当前抓取结果有误）

@author: ChangXing
@version: 1.2
@create: 2019.11.24
@revise: 2020.06.08
"""

import time

from selenium.common.exceptions import NoSuchElementException

import toolkit as tool


def crawler(live_list_path):
    browser = tool.open_chrome(use_user_dir=False)

    account_list = tool.file.load_as_string(live_list_path)
    for account_url in account_list.split("\n"):
        browser.get(account_url)

        time.sleep(3)

        text_subscribe = ""

        for _ in range(10):
            try:
                label_subscribe = browser.find_element_by_xpath('//*[@id="js-player-title"]/div/div[4]/div/span')
                if label_subscribe.text is not None and label_subscribe.text != "":
                    text_subscribe = label_subscribe.text
                    break
                time.sleep(1)
            except NoSuchElementException:
                time.sleep(1)

        print(account_url, text_subscribe)


if __name__ == "__main__":
    crawler("douyu_account_list.txt")  # 文件中为直播间Url列表
