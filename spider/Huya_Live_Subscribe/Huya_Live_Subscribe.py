import crawlertool as tool
from Selenium4R import Chrome


class SpiderHuyaLiveSubscribe(tool.abc.SingleSpider):
    """虎牙直播间订阅数爬虫"""

    def __init__(self, driver):
        self.driver = driver

    def running(self, live_url):
        self.driver.get(live_url)

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
