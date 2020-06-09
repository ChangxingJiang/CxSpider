"""
WeGame云顶之弈比赛记录爬虫：召唤师列表

@author: ChangXing
@version: 2.1
@create: 2019.12.10
@revise: 2020.06.09
"""

import os
import time

import requests

import environment as env
import toolkit as tool
from wegame import setting


def crawler(mysql):
    # 设置不需要代理的环境变量(解决request.exceptions.ProxyError:HTTPSConnectionPool的问题)
    os.environ["NO_PROXY"] = "qt.qq.com"

    # 请求召唤师列表
    num = 1
    for params_item in env.DATA["WeGame"]["TFT List"]:
        print("抓取召唤师列表:", num, "/", len(env.DATA["WeGame"]["TFT List"]))
        num += 1
        response = requests.get(
            url="https://qt.qq.com/lua/mlol_battle_info/get_total_tier_rank_list",
            params={"area_id": str(params_item[0]), "offset": str(params_item[1]), "sign": str(params_item[2])},
            verify=False)
        summoner_json = response.json()
        if "data" not in summoner_json:
            continue
        if "player_list" not in summoner_json["data"]:
            continue
        summoner_list = list()
        for summoner_item in summoner_json["data"]["player_list"]:
            if "tier_title" not in summoner_item:
                continue
            if "name" not in summoner_item:
                continue
            if "uuid" not in summoner_item:
                continue
            if "ranking" not in summoner_item:
                continue
            if "league_points" not in summoner_item:
                continue
            summoner_list.append({
                "tier": summoner_item["tier_title"],
                "name": summoner_item["name"],
                "uuid": summoner_item["uuid"],
                "area": 1,
                "ranking": summoner_item["ranking"],
                "points": summoner_item["league_points"],
                "period": setting.PERIOD
            })
        mysql.insert("summoner", summoner_list)
        time.sleep(3)


if __name__ == "__main__":
    crawler(tool.mysql_connect("TFT"))
