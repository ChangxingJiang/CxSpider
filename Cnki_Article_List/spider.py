"""
CNKI(中国知网)刊期包含论文列表爬虫

@Author: 长行
@Update: 2020.06.08
"""

import re

import crawlertool as tool
import requests
from bs4 import BeautifulSoup

from toolkit.textCleaner import TextCleaner


class SpiderCnkiArticleList(tool.abc.SingleSpider):
    """CNKI(中国知网)刊期包含论文列表爬虫"""

    def running(self, journal, pcode, pykm, year, issue):
        """采集指定刊期的论文列表

        :param journal: <str> 期刊名称
        :param pcode: <str> 中国知网期刊所属数据库
        :param pykm: <str> 中国知网期刊ID(主要ID)
        :param year: <int> 刊期所属年份
        :param issue: <int> 刊期在年份中的序号
        :return: <list:dict> 指定刊期的期刊论文列表
        """
        ajax_url = "http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year={}&issue={}&pykm={}&pageIdx=0&pcode={}"
        ajax_url = ajax_url.format(year, issue, pykm, pcode)
        response = requests.get(ajax_url)  # 请求获取期刊论文列表Ajax
        html_text = response.content.decode(errors="ignore")
        if html_text is None:
            return None
        bs = BeautifulSoup(html_text, "lxml")  # 将期刊论文列表Ajax转换为BeautifulSoup对象

        article_list = []  # 返回的期刊论文列表
        now_column = None  # 当前所处的栏目

        label_wrapper = bs.select_one("html > body")
        if label_wrapper is None:
            return None
        for article_label in bs.select_one("html > body").children:  # 循环处理论文及所处栏目
            if article_label.name == "dt":
                now_column = article_label.get_text()
            elif article_label.name == "dd":
                title = str(TextCleaner(article_label.select_one("dd > span > a").text).clear_empty())  # 读取论文标题
                href = article_label.select_one("dd > span > a")["href"]  # 读取论文链接
                if re.search("(?<=dbCode=)[^&]+(?=&)", href):
                    db_code = re.search("(?<=dbCode=)[^&]+(?=&)", href).group()  # 在论文链接中提取变量值
                else:
                    continue
                if re.search("(?<=filename=)[^&]+(?=&)", href):
                    file_name = re.search("(?<=filename=)[^&]+(?=&)", href).group()  # 在论文链接中提取变量值
                else:
                    continue
                if re.search("(?<=tableName=)[^&]+(?=&)", href):
                    db_name = re.search("(?<=tableName=)[^&]+(?=&)", href).group()  # 在论文链接中提取变量值
                else:
                    continue
                if "来稿要求" in title:
                    continue
                article_list.append({
                    "journal": journal,
                    "pcode": pcode,
                    "pykm": pykm,
                    "year": str(year),
                    "issue": str(issue),
                    "column": now_column,
                    "title": title,
                    "db_code": db_code,
                    "file_name": file_name,
                    "db_name": db_name
                })

        return article_list


if __name__ == "__main__":
    journal_list = {
        "CSSCI-新闻与传播学": [
            ["新闻与传播研究", "CJFD", "YANJ"],
            ["编辑学报", "CJFD", "BJXB"],
            ["编辑之友", "CJFD", "BJZY"],
            ["出版发行研究", "CJFD", "CBFX"],
            ["出版科学", "CJFD", "CBKX"],
            ["当代传播", "CJFD", "DACB"],
            ["国际新闻界", "CJFD", "GJXW"],
            ["科技与出版", "CJFD", "KJYU"],
            ["现代出版", "CJFD", "DXCB"],
            ["现代传播(中国传媒大学学报)", "CJFD", "XDCB"],
            ["新闻大学", "CJFD", "XWDX"],
            ["新闻记者", "CJFD", "XWJZ"],
            ["新闻界", "CJFD", "NEWS"],
            ["中国出版", "CJFD", "ZGCB"],
            ["中国科技期刊研究", "CJFD", "JYKQ"]
        ],
        "CSSCI扩展-新闻与传播学": [
            ["编辑学刊", "CJFD", "BJXZ"],
            ["出版广角", "CJFD", "CBGJ"],
            ["传媒", "CJFD", "CMEI"],
            ["电视研究", "CJFD", "DSYI"],
            ["全球传媒学刊", "CJFD", "QQCM"],
            ["新闻爱好者", "CJFD", "XWAH"
             ],
            ["新闻与传播评论", "CJFD", "WHDS"],
            ["新闻与写作", "CJFD", "XWXZ"],
            ["中国编辑", "CJFD", "BJZG"]
        ]
    }

    spider_cnki_article_list = SpiderCnkiArticleList()

    for journal_item in journal_list["CSSCI-新闻与传播学"]:
        print(journal_item[0], ":", spider_cnki_article_list.running(journal_item[0], journal_item[1], journal_item[2], "2020", "04"))
