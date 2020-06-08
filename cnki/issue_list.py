"""
知网期刊包含刊期列表爬虫

@author: ChangXing
@version: 1.1
@create: 2019.11.02
@revise: 2020.06.08
"""

import re

import requests
from bs4 import BeautifulSoup

import environment as env


def crawler(pcode, pykm):
    """ 获取期刊刊期列表
    :param pcode: <str> 中国知网期刊所属数据库
    :param pykm: <str> 中国知网期刊ID(主要ID)
    :return: <list:dict> 期刊刊期列表
    """
    ajax_url = "http://navi.cnki.net/knavi/JournalDetail/GetJournalYearList?pcode={}&pykm={}&pIdx=0".format(pcode, pykm)
    html_text = requests.get(ajax_url).content.decode(errors="ignore")  # 请求获取期刊刊期列表Ajax
    if html_text is None:
        print("获取期刊刊期列表失败!")
        return None
    bs = BeautifulSoup(html_text, 'lxml')  # 将期刊刊期列表Ajax转换为BeautifulSoup对象

    issue_list = []  # 返回的刊期列表
    for journal_label in bs.select("#page1 > div > dl > dd > a"):  # 定位到各个刊期的标签
        if match_name := re.search("[0-9]{6}", journal_label["id"]):  # 提取刊期名称，格式例如：yq201908
            journal_name = match_name.group()
            issue_list.append({
                "year": journal_name[0:4],
                "issue": journal_name[4:]
            })
    if len(issue_list) == 0:
        print("获取期刊刊期列表失败!")
        return None
    else:
        return issue_list


if __name__ == "__main__":
    for journal in env.DATA["Cnki"]["新闻与传播学"]:
        print(journal[0], ":", crawler(journal[1], journal[2]))
        break
