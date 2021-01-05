"""
斗鱼弹幕爬虫

需要第三方模块：
BeautifulSoup4 >= 4.9.0
Selenium4R >= 0.0.3
Utils4R >= 0.0.2

@author: ChangXing
@version: 1.2
@create: 2019.11.24
@revise: 2020.06.08

功能: 抓取直播间中所有弹幕，依据不同类型的弹幕提取不同信息，并存储于文件中
说明: 使用Selenium打开斗鱼直播间，通过浏览器不断将Js渲染后的网页源代码传给BeautifulSoup解析弹幕
目标Url: https://www.douyu.com/topic/s9lol?rid=288016
"""

import collections
import re
import time
from datetime import datetime

import crawlertool as tool
from Selenium4R import Chrome
from bs4 import BeautifulSoup


class SpiderDouyuLiveBarrage(tool.abc.LoopSpider):
    """斗鱼弹幕爬虫"""

    def __init__(self, driver, live_url, interval):
        super().__init__(interval)
        self.driver = driver
        self.live_url = live_url

        # 访问目标斗鱼主播的直播间
        self.driver.get(live_url)

        # 等待页面渲染完成
        time.sleep(10)

        self.barrage_id_list = collections.deque()

    def running(self):
        label_html = self.driver.find_element_by_id("js-barrage-list").get_attribute("innerHTML")
        soup = BeautifulSoup(label_html, "lxml")  # 将网页内容解析为Soup对象

        barrage_list = []
        for label in soup.select("li"):

            bid = str(label["id"])  # 提取:弹幕ID

            if bid in self.barrage_id_list:
                continue

            self.barrage_id_list.append(bid)

            if len(self.barrage_id_list) > 200:
                self.barrage_id_list.popleft()

            barrage_info = {
                "type": "",  # 弹幕所属类型
                "user_name": "",  # 弹幕发布者名称
                "user_level": 0,  # 弹幕发布者等级
                "content": "",  # 弹幕内容
                "text": "",  # 其他信息,
                "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 弹幕采集时间
            }

            type_class = label.select_one("li > div")["class"]
            if "Barrage-notice" in type_class and "normalBarrage" not in type_class:
                barrage_info["type"] = "NOTICE"
            elif "normalBarrage" in type_class:
                barrage_info["type"] = "NORMAL"
            elif "Barrage-userEnter" in type_class:
                barrage_info["type"] = "ENTER"
            elif "Barrage-message" in type_class:
                barrage_info["type"] = "MESSAGE"

            for info_label in label.select("li > div > span"):
                info_label_class = info_label["class"]
                if "UserLevel" in info_label_class:
                    barrage_info["user_level"] = re.search("[0-9]+", info_label["title"]).group()
                elif "Barrage-nickName" in info_label_class:
                    barrage_info["user_name"] = info_label.text.replace(" ", "")
                elif "Barrage-content" in info_label_class:
                    barrage_info["content"] = info_label.text.replace(" ", "")
                elif "Barrage-text" in info_label_class:
                    barrage_info["text"] = info_label.text.replace(" ", "")

            barrage_list.append(barrage_info)

        if len(barrage_list) < 200:
            self.write(barrage_list)
        else:
            print("本次时间范围内弹幕列表未自动向下滚动...")


# ------------------- 单元测试 -------------------
if __name__ == "__main__":
    class MySpider(SpiderDouyuLiveBarrage):
        """重写SpiderBilibiliLiveBarrage类"""

        def __init__(self, driver, live_url, mysql):
            super().__init__(driver=driver, live_url=live_url, interval=0.5)
            self.mysql = mysql

        def write(self, data):
            # 将结果写入到数据库
            self.mysql.insert(table="douyu_live", data=data)


    driver = Chrome(cache_path=r"E:\Temp")  # 打开Chrome浏览器
    spider = MySpider(driver=driver, live_url="https://www.douyu.com/96291", mysql=tool.db.DefaultMySQL())
    spider.start()
