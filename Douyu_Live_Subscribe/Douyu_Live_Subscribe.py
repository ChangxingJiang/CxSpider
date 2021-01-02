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

import crawlertool as tool
from Selenium4R import Chrome
from selenium.common.exceptions import NoSuchElementException


class SpiderDouyuLiveSubscribe(tool.abc.SingleSpider):
    """
    斗鱼直播间订阅数爬虫
    """

    def __init__(self, driver):
        self.driver = driver

    def running(self, account_url):
        self.driver.get(account_url)

        time.sleep(3)

        text_subscribe = ""

        for _ in range(10):
            try:
                label_subscribe = self.driver.find_element_by_xpath('//*[@id="js-player-title"]/div/div[4]/div/span')
                if label_subscribe.text is not None and label_subscribe.text != "":
                    text_subscribe = label_subscribe.text
                    break
                time.sleep(1)
            except NoSuchElementException:
                time.sleep(1)

        return [{
            "account_url": account_url,
            "text_subscribe": text_subscribe
        }]


# ------------------- 单元测试 -------------------
if __name__ == "__main__":
    driver = Chrome(cache_path=r"E:\Temp")
    print(SpiderDouyuLiveSubscribe(driver).running("https://www.douyu.com/96291"))
    driver.quit()
