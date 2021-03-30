"""
WanPlus英雄联盟比赛包含场次列表爬虫

@author: ChangXing
@version: 1.1
@create: 2020.04.20
@revise: 2020.06.08
"""

import crawlertool as tool
from bs4 import BeautifulSoup


class SpiderWanplusLolMatchList(tool.abc.SingleSpider):
    """WanPlus英雄联盟比赛包含场次列表爬虫"""

    # 比赛请求的url
    _RACE_LIST_URL = "https://www.wanplus.com/schedule/%s.html"

    # 比赛请求的Headers
    _RACE_LIST_HEADERS = {
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

    def running(self, race_id):
        match_id_list = []
        response = tool.do_request(self._RACE_LIST_URL % race_id, headers=self._RACE_LIST_HEADERS)
        bs = BeautifulSoup(response.content.decode(), 'lxml')
        game_labels = bs.select("body > div > div.content > div.left > div:nth-child(1) > div > a")
        for game_label in game_labels:
            if game_label.has_attr("data-matchid"):
                match_id_list.append(game_label["data-matchid"])
        return [{
            "race_id": race_id,
            "match_id_list": match_id_list
        }]


# ------------------- 单元测试 -------------------
if __name__ == "__main__":
    print(SpiderWanplusLolMatchList().running("67046"))
