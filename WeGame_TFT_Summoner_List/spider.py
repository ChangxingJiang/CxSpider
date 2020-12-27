"""
WeGame云顶之弈比赛记录爬虫：召唤师列表

需要第三方模块：
Utils4R >= 0.0.2

@author: ChangXing
@version: 2.1
@create: 2019.12.10
@revise: 2020.06.09
"""

import os
import time

import crawlertool as tool
import requests

from WeGame_TFT_Summoner_List import setting

TFT_LIST = [
    [1, 0, "a1a1eeafef7deb237f2f5e6172958615", "艾欧尼亚:第1页"],
    [1, 20, "c4deacb883f65f4680cb55d4e8e6d5fc", "艾欧尼亚:第2页"],
    [1, 40, "93be8e36d35b7a1265f1483217c9cc15", "艾欧尼亚:第3页"],
    [1, 60, "41879281bc8425c941c737c4ff3bde4a", "艾欧尼亚:第4页"],
    [1, 80, "eabfa2d2b60bcdf6a7fac54f68129dd6", "艾欧尼亚:第5页"],
    [1, 100, "19160e26e17143f1bb5539d55905819b", "艾欧尼亚:第6页"],
    [2, 0, "0d3349fa69a1d6055611880d03edffcc", "比尔吉沃特:第1页"],
    [6, 0, "7f97a096f76a405507af4e7f16dd0d35", "德玛西亚:第1页"],
    [14, 0, "c18788e78d9b059a556de576c78a334c", "黑色玫瑰:第1页"],
    [14, 20, "46b6c711db7d80a34b9278704583006d", "黑色玫瑰:第2页"]
]


class SpiderTftSummonerList(tool.abc.SingleSpider):
    def running(self, params_item):
        response = requests.get(
            url="https://qt.qq.com/lua/mlol_battle_info/get_total_tier_rank_list",
            params={"area_id": str(params_item[0]), "offset": str(params_item[1]), "sign": str(params_item[2])},
            verify=False)
        summoner_json = response.json()
        if "data" not in summoner_json:
            return None
        if "player_list" not in summoner_json["data"]:
            return None
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
        return summoner_list


def crawler(mysql):
    spider = SpiderTftSummonerList()

    # 设置不需要代理的环境变量(解决request.exceptions.ProxyError:HTTPSConnectionPool的问题)
    os.environ["NO_PROXY"] = "qt.qq.com"

    # 请求召唤师列表
    num = 1
    for params_item in TFT_LIST:
        print("抓取召唤师列表:", num, "/", len(TFT_LIST))
        num += 1

        summoner_list = spider.running(params_item)

        mysql.insert("summoner", summoner_list)
        time.sleep(3)


if __name__ == "__main__":
    crawler(tool.db.MySQL(host="", user="", password="", database=""))
