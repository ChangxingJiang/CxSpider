"""
WanPlus英雄联盟场次详细信息爬虫

@author: ChangXing
@version: 1.1
@create: 2020.04.20
@revise: 2020.06.08
"""

import json

import crawlertool as tool


class SpiderWanplusLolMatchInfo(tool.abc.SingleSpider):
    """
    WanPlus英雄联盟场次详细信息爬虫
    """

    # 场次请求的url
    _MATCH_LIST_URL = "https://www.wanplus.com/ajax/matchdetail/%s?_gtk=345357323"

    # 场次请求的headers中referer参数的值
    _MATCH_LIST_REFERER = "https://www.wanplus.com/schedule/%s.html"

    # 场次请求的headers
    _MATCH_LIST_HEADERS = {
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
    }

    def running(self, race_id, match_id):
        # 执行场次请求
        self._MATCH_LIST_HEADERS["referer"] = self._MATCH_LIST_REFERER % race_id
        response = tool.do_request(self._MATCH_LIST_URL % match_id, headers=self._MATCH_LIST_HEADERS)
        return [{
            "race_id": race_id,
            "match_id": match_id,
            "match_detail": json.loads(response.content.decode())
        }]


# ------------------- 单元测试 -------------------
if __name__ == "__main__":
    print(SpiderWanplusLolMatchInfo().running(race_id="67046", match_id="71690"))
