"""
起点中文网小说排行榜

@author: ChangXing
@version: 1.0
@create: 2020.08.09
@revise: -
"""

import requests
from bs4 import BeautifulSoup


def crawler():
    # 执行请求
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "hiijack=0; _yep_uuid=2aed8739-8cfd-667f-857f-e3fd74ad9d73; e1=%7B%22pid%22%3A%22qd_P_rank_06%22%2C%22eid%22%3A%22%22%7D; e2=%7B%22pid%22%3A%22qd_P_rank_06%22%2C%22eid%22%3A%22qd_C01%22%2C%22l1%22%3A4%7D; _csrfToken=XwEpsNMimKynhTEWQHcN1i3D13nZBOTYc20kJnFV; newstatisticUUID=1595512874_831604473; e2=%7B%22pid%22%3A%22qd_P_rank_05%22%2C%22eid%22%3A%22qd_C06%22%2C%22l1%22%3A4%7D; e1=%7B%22pid%22%3A%22qd_P_rank_01%22%2C%22eid%22%3A%22qd_C55%22%2C%22l1%22%3A5%7D",
        "Host": "www.qidian.com",
        "Pragma": "no-cache",
        "Referer": "https://www.qidian.com/rank/collect?style=2&chn=12&page=1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    }
    response = requests.get("https://www.qidian.com/rank/collect?style=2&chn=-1&page=1", headers=headers)

    # 解析答案
    bs = BeautifulSoup(response.content.decode(), 'lxml')
    for book_label in bs.select("#rank-view-list > div > table > tbody > tr"):
        print(book_label.select_one("tr > td:nth-child(2)").text.replace("「", "").replace("」", ""))


if __name__ == "__main__":
    crawler()
