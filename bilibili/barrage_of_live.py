"""
Bilibili弹幕爬虫

需要第三方模块：
BeautifulSoup4 >= 4.9.0
Selenium4R >= 0.0.3
Utils4R >= 0.0.6

@Author: ChangXing
@Update: 2020.10.18
"""

import time

import crawlertool as tool
from Selenium4R import Chrome
from bs4 import BeautifulSoup


class SpiderBilibiliBarrage(tool.abc.SingleSpider):
    """Bilibili弹幕爬虫"""

    def __init__(self, driver, live_url):
        """启动爬虫并打开目标Bilibili直播间

        :param driver: Selenium实例
        :param live_url: 目标Bilibili直播间地址
        """
        self.driver = driver
        self.live_url = live_url

        # 初始化当前抓取的最新推文的时间戳
        self.update_time = time.time()

        driver.get(live_url)  # 访问目标Bilibili主播的直播间
        time.sleep(10)

    def run(self):
        label_html = self.driver.find_element_by_id("chat-history-list").get_attribute("outerHTML")
        soup = BeautifulSoup(label_html, "lxml")

        barrage_list = []
        for label in soup.select("#chat-history-list > div"):

            barrage_info = {
                "user_name": "",  # 弹幕发布者名称
                "user_id": 0,  # 弹幕发布者等级
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
                    barrage_list.append(barrage_info)
                    self.update_time = temp_time

        return barrage_list


def crawler(live_name, live_url, mysql):
    driver = Chrome(cache_path=r"E:\Temp")  # 打开Chrome浏览器

    spider_bilibili_barrage = SpiderBilibiliBarrage(driver, live_url)

    # 创建目标数据表
    table_name = "bilibili_{}".format(time.strftime("%Y%m%d_%H%M", time.localtime(time.time())))
    sql_create = "CREATE TABLE live_barrage.`{}` (" \
                 "`bid` int(11) NOT NULL AUTO_INCREMENT COMMENT '弹幕ID(barrage id)'," \
                 "`type` varchar(60) DEFAULT NULL COMMENT '弹幕类型'," \
                 "`fetch_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '弹幕抓取时间(约等于弹幕发布时间)'," \
                 " `user_name` varchar(40) DEFAULT NULL COMMENT '弹幕发布者名称'," \
                 " `user_id` int(11) DEFAULT NULL COMMENT '弹幕发布者等级'," \
                 " `content` varchar(100) DEFAULT NULL COMMENT '弹幕内容'," \
                 " PRIMARY KEY (`bid`)" \
                 ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Bilibili弹幕({})';"
    mysql.create(sql_create.format(table_name, live_name))

    print("开始抓取Bilibili直播弹幕.....")

    total_time = 0
    total_num = 0

    barrage_num = 0

    for num in range(36000):
        start_time = time.time()
        barrage_list = spider_bilibili_barrage.run()
        mysql.insert(table_name, barrage_list)

        total_num += 1
        total_time += 1000 * (time.time() - start_time)

        wait_time = 0.5
        if wait_time > (time.time() - start_time):
            time.sleep(0.5 - (time.time() - start_time))

        barrage_num += len(barrage_list)

        print("本次时间范围内新增弹幕:", len(barrage_list), "条,", "(共计:", barrage_num, ")", "|",
              "运行时间:", round(total_time / total_num), "毫秒", "(", round(total_time), "/", total_num, ")")


if __name__ == "__main__":
    crawler(live_name="20191110_LOL世界赛决赛(FPX vs G2)",
            live_url="https://live.bilibili.com/blanc/6?liteVersion=true",
            mysql=tool.db.MySQL(host="", user="", password="", database=""))
