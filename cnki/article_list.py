"""
知网刊期包含论文列表爬虫

@author: ChangXing
@version: 1.1
@create: 2019.11.02
@revise: 2020.06.08
"""

import re

import requests
from bs4 import BeautifulSoup

import environment as env
from toolkit.textCleaner import TextCleaner


def crawler(journal, pcode, pykm, year, issue):
    """ 抓取指定刊期的期刊论文列表
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
    bs = BeautifulSoup(html_text, 'lxml')  # 将期刊论文列表Ajax转换为BeautifulSoup对象

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

    if len(article_list) == 0:
        return None
    else:
        return article_list


if __name__ == "__main__":
    for journal_item in env.DATA["Cnki"]["CSSCI"]["新闻与传播学"]:
        print(journal_item[0], ":", crawler(journal_item[0], journal_item[1], journal_item[2], "2020", "04"))
        break
