# coding:utf-8

"""
微博账号推文爬虫

@Update: 2020.10.23
"""

import json
import re
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import List

import crawlertool as tool


class SpiderWeiboPost(tool.abc.SingleSpider):
    def __init__(self):
        # 爬虫实例的常量
        self.default_domain = "107603"

        # 爬虫实例的变量
        self.user_id = None
        self.earliest_post = None

    def run(self, user_id: str, since_timestamp: int, until_timestamp: int) -> List[Dict]:
        """执行微博推文爬虫

        :param user_id: 微博账号ID
        :param since_timestamp: 抓取时间范围的右侧边界（最早时间戳）
        :param until_timestamp: 抓取时间范围的左侧边界（最晚时间戳）
        :return: 微博推文数据列表
        """
        # 初始化爬虫实例的变量
        self.user_id = user_id

        self.console("抓取开始,目标微博账号ID:" + user_id)

        post_list = []  # 推文列表
        maybe_finish = False  # 是否已包含可能的置顶推文

        for page in range(1, 1001):  # 请求参数中page=0和page=1均返回第1页（即page=1为第1页）
            # 计算实际请求的Ajax的Url
            actual_url = ("https://m.weibo.cn/api/container/getIndex?" +
                          "type=uid" +
                          "&value=" + user_id +
                          "&containerid=" + self.default_domain + user_id +
                          "&page=" + str(page))

            self.console("抓取开始,第" + str(page) + "次下拉,实际请求Url:" + actual_url)

            # 对Ajax执行请求
            response_text = tool.try_request(actual_url, headers={"User-Agent": tool.static.USER_AGENT["Win10_Chrome"]})
            if not response_text:
                self.log("抓取结束:Ajax请求结果为空")
                return post_list
            try:
                response_json = json.loads(response_text)["data"]["cards"]
            except (json.JSONDecodeError, KeyError):
                self.log("抓取结束:Ajax请求结果的数据格式异常(数据并非Json格式数据)")
                return post_list

            # 遍历解析推文数据
            for content in response_json[1:]:
                item = {}

                # 解析推文数据
                try:
                    content = content["mblog"]  # 微博账号内容信息全在这个标签之后
                    item["time"] = self.count_time_date(content["created_at"])
                    item["post_id"] = content["id"]
                    item["post_bid"] = content["bid"]
                    item["text"] = content["text"].replace("\n", ";")
                    item["likes"] = content["attitudes_count"]
                    item["comments"] = content["comments_count"]
                    item["reposts"] = content["reposts_count"]
                    item["if_repost"] = ("retweeted_status" in content)
                except KeyError:
                    self.log("抓取结束:Ajax请求结果的数据格式异常(Json格式数据结构异常)")
                    return post_list

                if "time" not in item or not item["time"] or until_timestamp <= item["time"]:
                    # 如果当前推文晚于抓取时间范围的右侧边界则跳过当前推文
                    continue
                elif since_timestamp <= item["time"] < until_timestamp:
                    # 如果当前推文处于抓取时间范围内则存储当前推文
                    post_list.append(item)
                elif maybe_finish:
                    # 如果当前推文早于抓取时间范围的左侧边界且已考虑可能的置顶推文则结束当前抓取
                    return post_list
                else:
                    # 如果当前推文早于抓取时间范围的左侧边界且未考虑可能的置顶推文则标记已考虑置顶推文
                    maybe_finish = True

            time.sleep(5)

        return post_list

    @staticmethod
    def count_time_date(time_source: str) -> int:
        """通过微博显示的推文发布时间换算时间戳

        形式1——今年以前发布：%Y-%m-%d（例如：2019-10-23）
        形式2——昨天以前、今年年内发布：%m-%d（例如：09-29）
        形式3——昨天、且距离当前超过24小时前发布：昨天
        形式4——距离当前1-24小时内发布：N小时前（例如：3小时前）
        形式5——距离当前1小时内发布：N分钟前（例如：27分钟前）
        """
        # 计算今天和昨天的零点的时间戳
        today = int(time.mktime(time.strptime((date.today()).strftime("%Y-%m-%d"), "%Y-%m-%d")))
        yesterday = int(time.mktime(time.strptime((date.today() + timedelta(days=-1)).strftime("%Y-%m-%d"), "%Y-%m-%d")))

        if time_source.count("-") == 2:  # 处理形式1
            return int(time.mktime(time.strptime(time_source, "%Y-%m-%d")))

        elif time_source.count("-") == 1:  # 处理形式2
            return int(time.mktime(time.strptime(str(datetime.now().year) + "-" + time_source, "%Y-%m-%d")))

        elif "昨天" in time_source:  # 处理形式3
            return yesterday

        elif "小时" in time_source:  # 处理形式4
            if pattern := re.search(r"\d+", time_source):
                if int(pattern.group()) > datetime.now().hour:
                    return yesterday
                else:
                    return today

        elif "分钟" in time_source:  # 处理形式5
            if pattern := re.search(r"\d+", time_source):
                if datetime.now().hour == 0 and int(pattern.group()) > datetime.now().minute:
                    return yesterday
                else:
                    return today
