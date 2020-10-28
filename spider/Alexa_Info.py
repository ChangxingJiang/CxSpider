# coding:utf-8

from typing import Dict

import Utils4R as Utils
from bs4 import BeautifulSoup


class SpiderAlexa(Utils.abc.SingleSpider):
    """Alexa网站信息爬虫

    爬虫逻辑为直接请求Alexa的包含指定网站数据的页面以获取数据；
    Alexa对于浏览量较小的网站，仅收录部分数据，因此对于这些我们网站我们也仅能采集到部分数据

    @Update: 2020.10.23
    """

    def __init__(self):
        # 爬虫实例的变量
        self.page_url = None

    def run(self, page_url: str) -> Dict:
        """执行Alexa爬虫

        :param page_url: 目标网站地址
        :return: 字典格式的Alexa数据
        """

        # 计算实际请求的Alexa页面Url
        actual_url = "https://www.alexa.com/siteinfo/{0}".format(page_url)

        self.console("抓取开始,实际请求Url:" + actual_url)

        item = {}

        # 执行请求
        response_text = Utils.try_request(actual_url)
        if not response_text:
            self.log("网站Url:" + page_url + "|请求失败，网络可能出现问题")
            return item

        bs = BeautifulSoup(response_text, "lxml")

        # 读取网站的Alexa排名
        if label := bs.select_one("#card_rank > section.rank > div.rank-global > div:nth-child(1) > div:nth-child(2) > p.big.data"):
            item["alexa_rank"] = Utils.extract.number(label.text)

        # 读取访客日均浏览页面数
        if label := bs.select_one("#card_metrics > section.engagement > div.flex > div:nth-child(1) > p.small.data"):
            item["pageviews"] = Utils.extract.number(label.text)
        if "pageviews" not in item or not item["pageviews"]:
            self.log("网站Url:" + page_url + "|访客日均浏览页面数抓取异常")

        # 读取访客日均浏览时长
        if label := bs.select_one("#card_metrics > section.engagement > div.flex > div:nth-child(2) > p.small.data"):
            item["daily_time"] = Utils.extract.number(label.text)
        if "daily_time" not in item or not item["daily_time"]:
            self.log("网站Url:" + page_url + "|访客日均浏览时长抓取异常")

        # 读取跳出率
        if label := bs.select_one("#card_metrics > section.engagement > div.flex > div:nth-child(2) > p.small.data"):
            item["bounce_rate"] = Utils.extract.number(label.text)
        if "bounce_rate" not in item or not item["bounce_rate"]:
            self.log("网站Url:" + page_url + "|跳出率抓取异常")

        # 读取同类网站平均跳出率
        if label := bs.select_one("#card_mini_competitors > section.group > div:nth-child(6) > div.ThirdFull.ProgressNumberBar > span"):
            item["avg_bounce_rate"] = Utils.extract.number(label.text)

        # 抓取用户地理分布
        country_list = []
        for label in bs.select("#countryName"):
            country_list.append(" ".join(label.text.split()[1:]))
        item["country_list"] = " > ".join(country_list)

        # 抓取外链数
        if label := bs.select_one("#card_metrics > section.linksin > div.enun > span.big.data"):
            item["links"] = Utils.extract.number(label.text)
        if "links" not in item or not item["links"]:
            self.log("网站Url:" + page_url + "|外链数抓取异常")

        # 抓取搜索引擎带来的访问占比
        if label := bs.select_one("#card_mini_competitors > section.group > div:nth-child(2) > div.ThirdFull.ProgressNumberBar > span"):
            item["search_traffic"] = Utils.extract.number(label.text)

        # 抓取同类型网站搜索引擎带来的访问占比
        if label := bs.select_one("#card_mini_competitors > section.group > div:nth-child(3) > div.ThirdFull.ProgressNumberBar > span"):
            item["avg_search_traffic"] = Utils.extract.number(label.text)

        # 抓取网站的关键词列表
        keyword_list = []
        for label in bs.select("#card_mini_topkw > section.table > div.Body > div"):
            keyword = label.select_one("div > div.keyword > span").text
            keyword_value = label.select_one("div > div.metric_one > span").text
            keyword_list.append(keyword + "(" + keyword_value + ")")
        item["keyword_list"] = " > ".join(keyword_list)

        return item
