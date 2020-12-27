"""
B站UP主发布视频列表爬虫

需要第三方模块：
Utils4R >= 0.0.6
requests >= 2.23.0

@Author: 长行
@Update: 2020.10.18
"""

import math
import time
from urllib.parse import urlencode

import crawlertool as tool


class SpiderBilibiliUserVideoList(tool.abc.SingleSpider):
    """B站UP主发布视频列表爬虫"""

    def __init__(self):
        # 执行请求的请求头
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "origin": "https://space.bilibili.com",
            "referer": "https://space.bilibili.com/20165629/video",
            "pragma": "no-cache",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Upgrade-Insecure-Requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        }

    def running(self, mid):
        # 执行请求的参数列表
        param_dict = {
            "mid": 20165629,
            "ps": 30,
            "tid": 0,
            "pn": 1,
            "keyword": "",
            "order": "pubdate",
            "jsonp": "jsonp",
        }

        now_page = 1
        max_page = 2

        video_list = []
        while now_page <= max_page:
            print("正在请求第", now_page, "页......")

            param_dict["pn"] = now_page  # 将当前页填入到参数列表中
            response = tool.do_request("https://api.bilibili.com/x/space/arc/search?" + urlencode(param_dict), headers=self.headers)
            response_json = response.json()  # 将返回结果解析为Json格式

            now_page += 1  # 页面累加
            max_page = math.ceil(response_json["data"]["page"]["count"] / 30)  # 获取UP主视频总数(用以控制翻页次数)

            for video_item in response_json["data"]["list"]["vlist"]:  # 遍历视频信息
                video_title = video_item["title"]  # 标题
                video_play = video_item["play"]  # 播放次数
                video_list.append((video_title, video_play))

            time.sleep(5)

        return video_list


if __name__ == "__main__":
    spider = SpiderBilibiliUserVideoList()
    print(spider.running(20165629))
