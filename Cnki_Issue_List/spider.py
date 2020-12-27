"""
CNKI(中国知网)期刊刊期列表爬虫

需要第三方模块：
requests >= 2.23.0
BeautifulSoup4 >= 4.9.0
Utils4R >= 0.0.6

@Author: 长行
@Update: 2020.06.08
"""

import re

import crawlertool as tool
from bs4 import BeautifulSoup


class SpiderCnkiIssueList(tool.abc.SingleSpider):
    """CNKI(中国知网)期刊刊期列表爬虫"""

    def running(self, pcode, pykm):
        """采集指定期刊的刊期列表

        :param pcode: <str> 中国知网期刊所属数据库
        :param pykm: <str> 中国知网期刊ID(主要ID)
        :return: <list:dict> 期刊刊期列表
        """
        issue_list = []

        ajax_url = "http://navi.cnki.net/knavi/JournalDetail/GetJournalYearList?pcode={}&pykm={}&pIdx=0".format(pcode, pykm)
        if html_text := tool.do_request(ajax_url).content.decode(errors="ignore"):  # 请求获取期刊刊期列表Ajax
            bs = BeautifulSoup(html_text, "lxml")  # 将期刊刊期列表Ajax转换为BeautifulSoup对象

            for journal_label in bs.select("#page1 > div > dl > dd > a"):  # 定位到各个刊期的标签
                if match_name := re.search("[0-9]{6}", journal_label["id"]):  # 提取刊期名称，格式例如：yq201908
                    journal_name = match_name.group()
                    issue_list.append({
                        "year": journal_name[0:4],
                        "issue": journal_name[4:]
                    })

        return issue_list


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
            ["新闻爱好者", "CJFD", "XWAH"],
            ["新闻与传播评论", "CJFD", "WHDS"],
            ["新闻与写作", "CJFD", "XWXZ"],
            ["中国编辑", "CJFD", "BJZG"]
        ]
    }

    spider_cnki_issue_list = SpiderCnkiIssueList()
    for journal in journal_list["CSSCI-新闻与传播学"]:
        print(journal[0], ":", spider_cnki_issue_list.running(journal[1], journal[2]))
