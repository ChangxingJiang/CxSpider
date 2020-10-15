"""
WanPlus英雄联盟场次详细信息爬虫

@author: ChangXing
@version: 1.1
@create: 2020.04.20
@revise: 2020.06.08
"""

import json
import os
import time

import requests

import Utils4R as Utils
from toolkit import environment as env

match_list_url = "https://www.wanplus.com/ajax/matchdetail/%s?_gtk=345357323"  # 场次请求的url
match_list_referer = "https://www.wanplus.com/schedule/%s.html"  # 场次请求的headers中referer参数的值
match_list_headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "referer": "",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "x-csrf-token": "345357323",
    "x-requested-with": "XMLHttpRequest"
}  # 场次请求的headers


def crawler():
    data_race = Utils.io.load_json(env.PATH["WanPlus"]["Race File"])  # 载入比赛包含场次表
    data_list_match = os.listdir(env.PATH["WanPlus"]["Match Path"])  # 载入游戏信息文件列表

    # 统计需要抓取的场次ID列表
    need_match_id_list = dict()
    for race_id, match_id_list in data_race.items():
        for match_id in match_id_list:
            match_file_name = str(match_id) + ".json"
            if match_file_name not in data_list_match:
                need_match_id_list[match_id] = race_id
    print("需要抓取的场次数量:", len(need_match_id_list))

    num = 1
    for match_id, race_id in need_match_id_list.items():
        print("正在抓取场次:", num, "/", len(need_match_id_list), "(", match_id, "-", race_id, ")")
        num += 1
        # 执行场次请求
        actual_url = match_list_url % match_id
        match_list_headers["referer"] = match_list_referer % race_id
        response = requests.get(actual_url, headers=match_list_headers)
        response_json = json.loads(response.content.decode())
        Utils.io.write_json(os.path.join(env.PATH["WanPlus"]["Match Path"], str(match_id) + ".json"), response_json)
        time.sleep(5)


if __name__ == "__main__":
    crawler()
