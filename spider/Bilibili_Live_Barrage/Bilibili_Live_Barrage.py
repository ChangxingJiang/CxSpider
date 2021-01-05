import time
from abc import ABCMeta

import crawlertool as tool
from Selenium4R import Chrome
from bs4 import BeautifulSoup


class SpiderBilibiliLiveBarrage(tool.abc.LoopSpider, metaclass=ABCMeta):
    """Bilibili弹幕爬虫"""

    def __init__(self, driver, live_url, interval):
        """启动爬虫并打开目标Bilibili直播间

        :param driver: Selenium实例
        :param live_url: 目标Bilibili直播间地址
        """
        super().__init__(interval)
        self.driver = driver
        self.live_url = live_url

        # 初始化当前抓取的最新推文的时间戳
        self.update_time = time.time()

        # 访问目标Bilibili主播的直播间
        driver.get(live_url)

        # 等待页面渲染完成
        time.sleep(10)

    def running(self):
        label_html = self.driver.find_element_by_id("chat-history-list").get_attribute("outerHTML")
        soup = BeautifulSoup(label_html, "lxml")

        barrage_list = []
        for label in soup.select("#chat-history-list > div > div"):
            print(label)

            barrage_info = {
                "user_name": "",  # 弹幕发布者名称
                "user_id": 0,  # 弹幕发布者ID
                "content": "",  # 弹幕内容
            }

            # 分析弹幕类型
            if "danmaku-item" in label["class"]:
                barrage_info["type"] = "NORMAL"
            elif "welcome-msg" in label["class"]:
                barrage_info["type"] = "ENTER"
            elif "system-msg" in label["class"]:
                barrage_info["type"] = "MESSAGE"
            elif "gift-item" in label["class"]:
                barrage_info["type"] = "GIFT"
            else:
                barrage_info["type"] = ""

            if barrage_info.get("type") == "NORMAL":
                temp_time = int(label["data-ts"])
                if temp_time >= self.update_time:
                    barrage_info["user_name"] = label["data-uname"]
                    barrage_info["user_id"] = label["data-uid"]
                    barrage_info["content"] = label["data-danmaku"]
                    barrage_info["fetch_time"] = temp_time
                    barrage_list.append(barrage_info)
                    self.update_time = temp_time

        self.write(barrage_list)


# ------------------- 单元测试 -------------------
if __name__ == "__main__":
    class MySpider(SpiderBilibiliLiveBarrage):
        """重写SpiderBilibiliLiveBarrage类"""

        def __init__(self, driver, live_url, mysql):
            super().__init__(driver=driver, live_url=live_url, interval=0.5)
            self.mysql = mysql

        def write(self, data):
            # 将结果写入到数据库
            self.mysql.insert(table="bilibili_live", data=data)


    driver = Chrome(cache_path=r"E:\Temp")  # 打开Chrome浏览器
    spider = MySpider(driver=driver, live_url="https://live.bilibili.com/732602", mysql=tool.db.DefaultMySQL())
    spider.start()
