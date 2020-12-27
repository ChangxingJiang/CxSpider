# coding:utf-8

"""
微博账号信息爬虫

@Update: 2020.10.23
"""

import json
from typing import Dict

import crawlertool as tool


class SpiderWeiboAccount(tool.abc.SingleSpider):
    def __init__(self):
        # 爬虫实例的变量
        self.user_id = None

    def running(self, user_id: str) -> Dict:
        """执行微博账号信息爬虫

        :param user_id: 微博账号的ID
        :return: Json格式的Twitter账号数据
        """
        self.user_id = user_id

        actual_url = "https://m.weibo.cn/api/container/getIndex?type=uid&value=" + str(user_id)

        self.console("开始抓取,实际请求的Url:" + actual_url)

        item = {}

        response_text = tool.try_request(actual_url, headers={"User-Agent": tool.static.USER_AGENT["Win10_Chrome"]})
        
        if not response_text:
            self.log("微博账号:" + str(user_id) + "|账号信息API请求失败")

        try:
            response_json = json.loads(response_text)

            # 读取微博账号的粉丝数
            item["followers"] = response_json["data"]["userInfo"]["followers_count"]

            # 读取微博账号微博的Domain值
            for tab in response_json["data"]["tabsInfo"]["tabs"]:
                if tab["id"] == 2:
                    item["domain"] = tab["containerid"][:6]
                    break
        except (json.decoder.JSONDecodeError, KeyError):
            self.log("微博账号:" + str(user_id) + "|账号信息API内容格式异常")

        return item
