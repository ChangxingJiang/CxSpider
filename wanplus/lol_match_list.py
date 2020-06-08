"""
WanPlus英雄联盟比赛包含场次列表爬虫

@author: ChangXing
@version: 1.1
@create: 2020.04.20
@revise: 2020.06.08
"""

import time

import requests
from bs4 import BeautifulSoup

import environment as env
import toolkit as tool

# 请求信息
race_list_url = "https://www.wanplus.com/schedule/%s.html"  # 比赛请求的url
race_list_headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "referer": "https://www.wanplus.com/lol/schedule",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
}


def crawler():
    data_date = tool.file.load_as_json(env.PATH["WanPlus"]["Date File"])  # 载入日期比赛表
    data_race = tool.file.load_as_json(env.PATH["WanPlus"]["Race File"])  # 载入比赛包含场次表

    # 统计需要抓取的比赛ID列表
    need_race_id_list = list()
    for date_name, date_race_list in data_date.items():
        for race_item in date_race_list:
            if race_item["race_id"] not in data_race:
                need_race_id_list.append(race_item["race_id"])
    print("需要抓取的比赛数量:", len(need_race_id_list))

    # 抓取需要的比赛数据
    for i in range(len(need_race_id_list)):
        need_race_id = str(need_race_id_list[i])
        print("正在抓取比赛:", i + 1, "/", len(need_race_id_list), "(", need_race_id, ")")
        match_id_list = list()  # 场次ID列表
        response = requests.get(race_list_url % need_race_id, headers=race_list_headers)
        bs = BeautifulSoup(response.content.decode(), 'lxml')
        game_labels = bs.select("body > div > div.content > div.left > div:nth-child(1) > div > a")
        for game_label in game_labels:
            if game_label.has_attr("data-matchid"):
                match_id_list.append(game_label["data-matchid"])
        data_race[need_race_id] = match_id_list
        tool.file.write_json(env.PATH["WanPlus"]["Race File"], data_race)  # 存储日期比赛表
        time.sleep(tool.get_scope_random(5))


if __name__ == "__main__":
    crawler()
