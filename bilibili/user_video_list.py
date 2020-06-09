"""
B站UP主发布视频列表爬虫

@author: ChangXing
@version: 1.0
@create: 2020.05.29
@revise: -
"""

import math
import time
from urllib.parse import urlencode

import requests

headers = {
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
}  # Headers

param_dict = {
    "mid": 20165629,
    "ps": 30,
    "tid": 0,
    "pn": 1,
    "keyword": "",
    "order": "pubdate",
    "jsonp": "jsonp",
}  # 参数列表


def crawler():
    now_page = 1
    max_page = 2
    while now_page <= max_page:
        print("正在请求第", now_page, "页......")
        param_dict["pn"] = now_page  # 将当前页填入到参数列表中
        response = requests.get("https://api.bilibili.com/x/space/arc/search?" + urlencode(param_dict), headers=headers)
        response_json = response.json()  # 将返回结果解析为Json格式

        now_page += 1  # 页面累加
        max_page = math.ceil(response_json["data"]["page"]["count"] / 30)  # 获取UP主视频总数(用以控制翻页次数)

        for video_item in response_json["data"]["list"]["vlist"]:  # 遍历视频信息
            video_title = video_item["title"]  # 标题
            video_play = video_item["play"]  # 播放次数
            print("标题:", video_title)
            print("播放次数:", video_play)

        time.sleep(5)


if __name__ == "__main__":
    crawler()
