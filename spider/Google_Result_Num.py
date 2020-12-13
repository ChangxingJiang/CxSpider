# coding:utf-8

"""
Google搜索引擎收录增量爬虫

@Update: 2020.10.22
"""

import calendar
import re
import time
from typing import Dict
from urllib import parse

import crawlertool as tool
from Selenium4R import Chrome


class SpiderGoogle(tool.abc.SingleSpider):
    def __init__(self, driver: "Chrome"):
        self.driver = driver

        # 爬虫实例的变量
        self.domain_name = None

    @staticmethod
    def get_domain_name(page_url: str) -> str:
        """提取网站的一级/二级域名

        :param page_url: 网站的任意页Url
        :return: 网站的一级/二级域名
        """
        page_url = re.sub(r"[Hh][Tt][Tt][Pp][Ss]?://", "", page_url)
        return page_url[:page_url.index("/")] if "/" in page_url else page_url

    def run(self, domain_name: str, year: int, month: int) -> Dict:
        """执行Google搜索引擎收录增量爬虫

        抓取Google收录在来自目标网站在目标年份和月份的结果数量

        :param domain_name: 网站的一级/二级域名（可以通过get_domain_name获取）
        :param year: 目标年份
        :param month: 目标月份
        :return Google搜索引擎收录增量数据
        """

        # 整理目标Url的格式信息
        self.domain_name = domain_name

        # 计算目标月份的最后一天的日期数
        last_date = calendar.monthrange(year, month)[1]

        # 计算指定Url（Alexa中包含目标信息的Url）
        actual_url = "https://www.google.com.hk/search?" + parse.urlencode({
            "q": "site:{}".format(domain_name),
            "eggs": "",
            "bacon": "strict",
            "source": "lnt",
            "tbs": "cdr:1,cd_min:{1}/1/{0},cd_max:{1}/{2}/{0}&tbm=".format(year, month, last_date),
            "tbm": ""
        })

        self.console("抓取开始,实际请求的Google页面Url:" + actual_url)

        # 打开指定Url
        self.driver.get(actual_url)

        # 模拟点击“搜索”
        if label := self.driver.find_element_by_css_selector("#tsf > div:nth-child(2) > div.A8SBwf > div.RNNXgb > button"):
            label.click()
            time.sleep(2)
        else:
            self.console("模拟点击“搜索”失败")

        # 模拟点击“工具”
        if label := self.driver.find_element_by_css_selector("#hdtb-tls"):
            label.click()
            time.sleep(2)
        else:
            self.console("模拟点击“工具”失败")

        # 解析搜索引擎收录增量并返回
        if label := self.driver.find_element_by_id("result-stats"):
            if pattern := re.search(r"[\d,]+\.?\d*", label.text):
                self.log("抓取成功(实际请求的Google页面Url:" + actual_url + ")")
                return {"web_post_sum": int(pattern.group().replace(",", ""))}
            else:
                self.log("抓取失败,获取的目标数据格式异常(实际请求的Google页面Url:" + actual_url + ")")
                return {"web_post_sum": None}
        else:
            self.log("抓取失败,未找到目标数据所在的节点(实际请求的Google页面Url:" + actual_url + ")")
            return {"web_post_sum": None}
