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

import crawlertool as tool
from Selenium4R import Chrome


class SpiderHuyaLiveSubscribe(tool.abc.SingleSpider):
    """
    虎牙直播间订阅数爬虫

    最近有效性检验：2020.12.28
    """

    def __init__(self, driver):
        self.driver = driver

    def running(self, account_url):
        self.driver.get(account_url)

        item = {
            "text_id": "",
            "text_subscribe": ""
        }

        # 读取直播间订阅数量
        if label_subscribe := self.driver.find_element_by_xpath('//*[@id="activityCount"]'):
            item["text_subscribe"] = label_subscribe.text

        # 读取直播间ID
        if label_id := self.driver.find_element_by_css_selector(
                "#J_roomHeader > div.room-hd-l > div.host-info > div.host-detail.J_roomHdDetail > span.host-rid"):
            item["text_id"] = label_id.text

        return [item]


# ------------------- 单元测试 -------------------
if __name__ == "__main__":
    driver = Chrome(cache_path=r"E:\temp")
    print(SpiderHuyaLiveSubscribe(driver).running("https://www.huya.com/102411"))
    driver.quit()
