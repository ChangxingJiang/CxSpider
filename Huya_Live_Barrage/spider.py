"""
虎牙直播弹幕爬虫

需要第三方模块：
BeautifulSoup4 >= 4.9.0
Selenium4R >= 0.0.3
Utils4R >= 0.0.2


@author: ChangXing
@version: 1.2
@create: 2019.11.24
@revise: 2020.06.08

功能: 抓取虎牙直播间中所有弹幕，依据不同类型的弹幕提取不同信息，并存储于文件中
说明: 使用Selenium打开虎牙直播间，通过浏览器不断将Js渲染后的网页源代码传给BeautifulSoup解析弹幕
目标Url: https://www.huya.com/%s
"""

import time

import crawlertool as tool
from Selenium4R import Chrome
from bs4 import BeautifulSoup


class SpiderHuyaBarrage(tool.abc.LoopSpider):
    def __init__(self, interval, live_name, live_url, mysql):
        super().__init__(interval)
        self.browser = Chrome(cache_path=r"E:\temp")
        self.browser.get(live_url)  # 访问目标虎牙主播的直播间

        self.mysql = mysql

        time_string = time.strftime("%Y%m%d_%H%M", time.localtime(time.time()))
        self.table_name = "huya_{}".format(time_string)

        sql_create = "CREATE TABLE live_barrage.`huya_{}` (" \
                     "`bid` int(11) NOT NULL AUTO_INCREMENT COMMENT '弹幕ID(barrage id)'," \
                     "`type` char(10) DEFAULT NULL COMMENT '弹幕类型'," \
                     "`fetch_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '弹幕抓取时间(约等于弹幕发布时间)'," \
                     " `user_name` varchar(40) DEFAULT NULL COMMENT '弹幕发布者名称'," \
                     " `user_noble` int(11) DEFAULT NULL COMMENT '弹幕发布者贵族等级'," \
                     " `content` varchar(100) DEFAULT NULL COMMENT '弹幕内容'," \
                     " `gift_name` varchar(40) DEFAULT NULL COMMENT '赠送礼物名称'," \
                     " `gift_num` int(11) DEFAULT '0' COMMENT '赠送礼物数量'," \
                     " `other` varchar(60) DEFAULT NULL COMMENT '弹幕其他信息'," \
                     " PRIMARY KEY (`bid`)" \
                     ") ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='虎牙弹幕({})';"
        self.mysql.create(sql_create.format(time_string, live_name))

        print("开始抓取虎牙直播弹幕.....")

        self.total_time = 0
        self.total_num = 0

        self.data_id_max = 0

    def running(self):
        for num in range(int(36000 / 0.5)):

            start_time = time.time()

            label_html = self.browser.find_element_by_id("chat-room__list").get_attribute("innerHTML")
            bs = BeautifulSoup(label_html, 'lxml')  # 将网页内容解析为Soup对象

            barrage_list = []
            for label in bs.select("li"):
                data_id = int(label["data-id"])  # 提取:弹幕ID

                if data_id <= self.data_id_max:  # 依据弹幕的ID判断弹幕是否还未抓取
                    if data_id > self.data_id_max - 101:
                        continue
                self.data_id_max = data_id

                barrage_info = {
                    "bid": data_id,  # 弹幕ID
                    "type": "",  # 弹幕所属类型
                    "user_name": "",  # 弹幕发布者名称
                    "user_noble": 0,  # 弹幕发布者贵族等级
                    "content": "",  # 弹幕内容
                    "gift_name": "",  # 礼物名称
                    "gift_num": 0,  # 礼物数量
                    "other": ""  # 其他信息
                }

                category = str(label.select_one("li > div")["class"])  # 提取:弹幕类型
                if "msg-smog" in category:  # 处理smog类型弹幕(普通弹幕)
                    barrage_info["type"] = "SG"
                    barrage_info["user_name"] = label.select_one("li > div > span:nth-child(1)").text
                    barrage_info["content"] = label.select_one("li > div > span:nth-child(3)").text
                elif "msg-normal" in category:  # 处理普通类型弹幕(普通弹幕)
                    barrage_info["type"] = "NM"
                    barrage_info["user_name"] = label.select_one("li > div > span:nth-child(2)").text
                    barrage_info["content"] = label.select_one("li > div > span:nth-child(5)").text
                elif "msg-nobleEnter" in category:  # 处理nobleEnter类型弹幕(贵族进入弹幕)
                    barrage_info["type"] = "NE"
                    barrage_info["user_name"] = label.select_one("li > div > div > p > span:nth-child(1)").text
                    barrage_info["user_noble"] = label.select_one("li > div > div")["class"]
                    barrage_info["content"] = "驾临直播间"
                elif "msg-nobleSpeak" in category:  # 处理nobleSpeak类型弹幕(贵族发言)
                    barrage_info["type"] = "NS"
                    barrage_info["user_name"] = label.select_one("li > div > p > span:nth-child(2)").text
                    barrage_info["user_noble"] = int(label.select_one("li > div")["class"])
                    barrage_info["content"] = label.select_one("li > div > p > span:nth-child(5)").text
                elif "tit-h-send" in category:  # 处理send类型提示(礼物赠送提示)
                    barrage_info["type"] = "SD"
                    barrage_info["user_name"] = label.select_one("li > div > span:nth-child(1)").text
                    barrage_info["gift_name"] = label.select_one("li > div > span:nth-child(3) > img")["alt"]
                    barrage_info["gift_num"] = int(label.select_one("li > div > span:nth-child(4) > img").text)
                elif "msg-onTVLottery" in category:
                    barrage_info["type"] = "TV"
                    barrage_info["user_name"] = label.select_one("li > div > span:nth-child(2)").text
                    barrage_info["content"] = label.select_one("li > div > div > span").text
                elif "msg-auditorSys" in category:  # 处理msg-auditorSys类型提示(系统提示)
                    barrage_info["type"] = "AS"
                    barrage_info["other"] = label.text
                elif "msg-sys" in category:  # 处理msg-sys类型提示(系统提示)
                    barrage_info["type"] = "SY"
                    barrage_info["other"] = label.text
                else:  # 处理其他类型
                    barrage_info.update(type="OT", other="弹幕名称" + category)
                barrage_list.append(barrage_info)

            self.write(barrage_list)

            self.total_num += 1
            self.total_time += 1000 * (time.time() - start_time)

            print("本次时间范围内新增弹幕:", len(barrage_list), "条,", "(共计:", self.data_id_max, ")", "|",
                  "运行时间:", round(self.total_time / self.total_num), "毫秒", "(", round(self.total_time), "/", self.total_num, ")")

    def write(self, data):
        self.mysql.insert(self.table_name, data)


if __name__ == "__main__":
    spider = SpiderHuyaBarrage(interval=0.5,
                               live_name="神超",
                               live_url="https://www.huya.com/102411",
                               mysql=tool.db.MySQL(host="", user="", password="", database=""))
    spider.start()
