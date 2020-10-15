"""
Bilibili弹幕爬虫

需要第三方模块：
BeautifulSoup4 >= 4.9.0
Selenium4R >= 0.0.3
Utils4R >= 0.0.2

@author: ChangXing
@version: 1.2
@create: 2019.11.24
@revise: 2020.06.08

功能: 抓取直播间中所有弹幕，依据不同类型的弹幕提取不同信息，并存储于文件中
说明: 使用Selenium打开Bilibili直播间，通过浏览器不断将Js渲染后的网页源代码传给BeautifulSoup解析弹幕
目标Url: https://www.bilibili.com/topic/s9lol?rid=288016
"""

import time

import Utils4R as Utils
from Selenium4R import Chrome
from bs4 import BeautifulSoup


def crawler(live_name, live_url, mysql):
    driver = Chrome(cache_path=r"E:\Temp")  # 打开Chrome浏览器
    driver.get(live_url)  # 访问目标Bilibili主播的直播间
    time.sleep(10)

    time_string = time.strftime("%Y%m%d_%H%M", time.localtime(time.time()))

    table_name = "bilibili_{}".format(time_string)
    sql_create = "CREATE TABLE live_barrage.`bilibili_{}` (" \
                 "`bid` int(11) NOT NULL AUTO_INCREMENT COMMENT '弹幕ID(barrage id)'," \
                 "`type` varchar(60) DEFAULT NULL COMMENT '弹幕类型'," \
                 "`fetch_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '弹幕抓取时间(约等于弹幕发布时间)'," \
                 " `user_name` varchar(40) DEFAULT NULL COMMENT '弹幕发布者名称'," \
                 " `user_id` int(11) DEFAULT NULL COMMENT '弹幕发布者等级'," \
                 " `content` varchar(100) DEFAULT NULL COMMENT '弹幕内容'," \
                 " PRIMARY KEY (`bid`)" \
                 ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Bilibili弹幕({})';"
    mysql.create(sql_create.format(time_string, live_name))

    print("开始抓取Bilibili直播弹幕.....")

    total_time = 0
    total_num = 0

    update_time = 0

    data_id_max = 0
    for num in range(int(36000 / 0.5)):

        start_time = time.time()

        label_html = driver.find_element_by_id("chat-history-list").get_attribute("outerHTML")

        soup = BeautifulSoup(label_html, 'lxml')  # 将网页内容解析为Soup对象

        barrage_list = []
        for label in soup.select("#chat-history-list > div"):

            barrage_info = {
                "type": "",  # 弹幕所属类型
                "user_name": "",  # 弹幕发布者名称
                "user_id": 0,  # 弹幕发布者等级
                "content": "",  # 弹幕内容
            }

            type_class = label["class"]

            if "danmaku-item" in type_class:
                barrage_info["type"] = "NORMAL"
            elif "welcome-msg" in type_class:
                barrage_info["type"] = "ENTER"
            elif "system-msg" in type_class:
                barrage_info["type"] = "MESSAGE"
            elif "gift-item" in type_class:
                barrage_info["type"] = "GIFT"

            if barrage_info.get("type") == "NORMAL":
                temp_time = int(label["data-ts"])
                if temp_time >= update_time:
                    update_time = temp_time
                    barrage_info["user_name"] = label["data-uname"]
                    barrage_info["user_id"] = label["data-uid"]
                    barrage_info["content"] = label["data-danmaku"]
                    barrage_list.append(barrage_info)

        mysql.insert(table_name, barrage_list)

        total_num += 1
        total_time += 1000 * (time.time() - start_time)

        wait_time = 0.5
        if wait_time > (time.time() - start_time):
            time.sleep(0.5 - (time.time() - start_time))

        data_id_max += len(barrage_list)

        print("本次时间范围内新增弹幕:", len(barrage_list), "条,", "(共计:", data_id_max, ")", "|",
              "运行时间:", round(total_time / total_num), "毫秒", "(", round(total_time), "/", total_num, ")")


if __name__ == "__main__":
    crawler(live_name="20191110_LOL世界赛决赛(FPX vs G2)",
            live_url="https://live.bilibili.com/blanc/6?liteVersion=true",
            mysql=Utils.db.MySQL(host="", user="", password="", database=""))
