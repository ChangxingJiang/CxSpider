"""
微博热搜榜爬虫

@author: ChangXing
@version: 1.1
@create: 2020.05.29
@revise: 2020.06.08
"""

import re
from abc import ABCMeta
from abc import abstractmethod

import crawlertool as tool
from bs4 import BeautifulSoup


class SpiderWeiboHotRanking(tool.abc.LoopSpider, metaclass=ABCMeta):
    _HEADERS = {
        "Accept": "text/html,application/xhtml+xrequestsml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "s.weibo.com",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
    }

    def running(self):
        # 执行网页请求
        response = tool.do_request("https://s.weibo.com/top/summary", headers=self._HEADERS)  # 请求微博热搜榜
        bs = BeautifulSoup(response.content.decode(errors="ignore"), "lxml")

        # 解析网页
        hot_list = []
        empty_rank = 0  # 统计空热搜(广告热搜)数量
        for label_item in bs.select("#pl_top_realtimehot > table > tbody > tr"):  # 遍历热搜的标签
            # 提取热搜排名
            if label_rank := label_item.select_one("tr > td.td-01"):
                if len(label_rank.text) == 0:
                    continue
                if match_rank := re.search("[0-9]+", label_rank.text):
                    ranking = int(match_rank.group()) - empty_rank
                else:
                    tool.console("报错", "提取的热搜排名不包含数字!")
                    continue
            else:
                tool.console("报错", "未提取到热搜排名!")
                continue

            # 提取热搜关键词
            if label_keyword := label_item.select_one("tr > td.td-02 > a"):
                keyword = label_keyword.text
            else:
                tool.console("报错", "未提取到热搜关键词!")
                continue

            # 提取热搜热度
            if label_heat := label_item.select_one("tr > td.td-02 > span"):
                if match_heat := re.search("[0-9]+", label_heat.text):
                    heat = int(match_heat.group())
                else:
                    tool.console("报错", "提取的热搜热度不包含数字!")
                    continue
            else:
                tool.console("报错", "未提取到热搜热度!")
                continue

            # 提取热搜标注
            if label_icon := label_item.select_one("tr > td.td-03"):
                icon = label_icon.text
                if icon == "荐":  # 跳过空热搜(广告热搜)
                    empty_rank += 1
                    continue
            else:
                tool.console("报错", "未提取到热搜标注标签!")
                continue

            hot_list.append({
                "ranking": ranking,
                "keyword": keyword,
                "heat": heat,
                "icon": icon
            })

        self.write(hot_list)

    @abstractmethod
    def write(self, data):
        """将结果写入到数据库"""
