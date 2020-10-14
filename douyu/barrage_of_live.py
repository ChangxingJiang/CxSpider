"""
斗鱼弹幕爬虫

需要第三方模块：
BeautifulSoup4 >= 4.9.0
Selenium4R >= 0.0.3

@author: ChangXing
@version: 1.2
@create: 2019.11.24
@revise: 2020.06.08

功能: 抓取直播间中所有弹幕，依据不同类型的弹幕提取不同信息，并存储于文件中
说明: 使用Selenium打开斗鱼直播间，通过浏览器不断将Js渲染后的网页源代码传给BeautifulSoup解析弹幕
目标Url: https://www.douyu.com/topic/s9lol?rid=288016
"""

import re
import time

from Selenium4R import Chrome
from bs4 import BeautifulSoup

from toolkit import mysql


def crawler(live_name, live_url, mysql):
    browser = Chrome(cache_path=r"E:\Temp")  # 打开Chrome浏览器
    browser.get(live_url)  # 访问目标斗鱼主播的直播间
    time.sleep(10)

    time_string = time.strftime("%Y%m%d_%H%M", time.localtime(time.time()))
    table_name = "douyu_{}".format(time_string)

    sql_create = "CREATE TABLE live_barrage.`douyu_{}` (" \
                 "`bid` int(11) NOT NULL AUTO_INCREMENT COMMENT '弹幕ID(barrage id)'," \
                 "`type` varchar(60) DEFAULT NULL COMMENT '弹幕类型'," \
                 "`fetch_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '弹幕抓取时间(约等于弹幕发布时间)'," \
                 " `user_name` varchar(40) DEFAULT NULL COMMENT '弹幕发布者名称'," \
                 " `user_level` int(11) DEFAULT NULL COMMENT '弹幕发布者等级'," \
                 " `content` varchar(100) DEFAULT NULL COMMENT '弹幕内容'," \
                 " `text` varchar(100) DEFAULT NULL COMMENT '弹幕其他信息'," \
                 " PRIMARY KEY (`bid`)" \
                 ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='斗鱼弹幕({})';"
    mysql.create(sql_create.format(time_string, live_name))

    print("开始抓取斗鱼直播弹幕.....")

    total_time = 0
    total_num = 0
    # screenshot = 0

    barrage_id_list = list()

    data_id_max = 0
    for num in range(int(36000 / 0.5)):

        start_time = time.time()

        label_html = browser.find_element_by_id("js-barrage-list").get_attribute("innerHTML")
        soup = BeautifulSoup(label_html, 'lxml')  # 将网页内容解析为Soup对象

        barrage_list = []
        for label in soup.select("li"):

            bid = str(label["id"])  # 提取:弹幕ID

            if bid in barrage_id_list:
                continue
            barrage_id_list.append(bid)

            if len(barrage_id_list) > 200:
                barrage_id_list.remove(barrage_id_list[0])

            barrage_info = {
                "type": "",  # 弹幕所属类型
                "user_name": "",  # 弹幕发布者名称
                "user_level": 0,  # 弹幕发布者等级
                "content": "",  # 弹幕内容
                "text": ""  # 其他信息
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

            mysql.insert(table_name, barrage_list)

            total_num += 1
            total_time += 1000 * (time.time() - start_time)

            print("本次时间范围内新增弹幕:", len(barrage_list), "条,", "(共计:", data_id_max, ")", "|",
                  "运行时间:", round(total_time / total_num), "毫秒", "(", round(total_time), "/", total_num, ")")

        else:

            total_num += 1
            total_time += 1000 * (time.time() - start_time)

            print("本次时间范围内弹幕列表未自动向下滚动...")

        wait_time = 0.5
        if wait_time > (time.time() - start_time):
            time.sleep(0.5 - (time.time() - start_time))

        data_id_max += len(barrage_list)


if __name__ == "__main__":
    crawler("东北大鹌鹑", "https://www.douyu.com/96291", mysql.connect("Barrage"))
