"""
豆瓣TOP250电影采集

@author: ChangXing
@version: 1.0
@create: 2020.05.28
@revise: -
"""

import re
import time

import crawlertool as tool
from bs4 import BeautifulSoup


class SpiderDoubanMovieTop250(tool.abc.SingleSpider):
    """
    豆瓣TOP250电影采集

    最近有效性检验日期 : 2020.12.28
    """

    _HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "Connection": "keep-alive",
        "host": "movie.douban.com",
        "pragma": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    }

    def running(self):
        movie_list = []

        for page_num in range(10):
            url = "https://movie.douban.com/top250?start={0}&filter=".format(page_num * 25)

            response = tool.do_request(url, headers=self._HEADERS)
            bs = BeautifulSoup(response.content.decode(errors="ignore"), 'lxml')

            for movie_label in bs.select("#content > div > div.article > ol > li"):  # 定位到电影标签
                # 获取电影链接(<a>标签的href属性)
                url = movie_label.select_one("li > div > div.pic > a")["href"]

                # 解析标题行
                title_text = movie_label.select_one("li > div > div.info > div.hd > a").text.replace("\n",
                                                                                                     "")  # 提取标题行内容+清除换行符
                title_chinese = title_text.split("/")[0].strip()  # 提取中文标题+清除前后空格
                title_other = [title.strip() for title in title_text.split("/")[1:]]  # 提取其他标题+清除前后空格

                # 解析内容信息(因长度原因，大部分主演名字不全暂不解析)
                info_text = movie_label.select_one("li > div > div.info > div.bd > p:nth-child(1)").text  # 获取说明部分内容
                info_text = re.sub("\n *", "\n", info_text)  # 清除行前多余的空格
                info_text = re.sub("^\n", "", info_text)  # 清除开头的空行
                info_line_1, info_line_2 = info_text.split("\n")[0:2]  # 获取第1行内容信息:包括导演和主演、获取第2行内容信息:包括年份、国家和类型
                director = re.sub(" *(主演|主\\.{3}|\\.{3}).*$", "", info_line_1)  # 仅保留导演部分
                year = int(re.search("[0-9]+", info_line_2.split("/")[0]).group())  # 提取电影年份并转换为数字
                country = info_line_2.split("/")[1].strip() if len(info_line_2.split("/")) >= 2 else None  # 提取电影国家
                classify = info_line_2.split("/")[2].strip() if len(info_line_2.split("/")) >= 3 else None  # 提取电影类型
                classify = re.split(" +", classify)  # 将电影类型转换为list形式

                # 解析评分
                rating_num = movie_label.select_one("li > div > div.info > div.bd > div > span.rating_num").text  # 提取评分
                rating_num = float(re.search("[0-9.]+", rating_num).group())  # 将评分转换为浮点型数字

                # 解析评分人数
                rating_people = movie_label.select_one("li > div > div.info > div.bd > div > span:nth-child(4)").text  # 提取评分人数
                rating_people = int(re.search("[0-9]+", rating_people).group())  # 将评分人数转换为数字

                # 解析评价(该标签可能会不存在)
                if quote_label := movie_label.select_one("li > div > div.info > div.bd > p.quote"):
                    quote = quote_label.text.replace("\n", "")  # 提取评价+清除换行符
                else:
                    quote = None

                movie_list.append({
                    "url": url,
                    "title_chinese": title_chinese,
                    "title_others": title_other,
                    "director": director,
                    "year": year,
                    "country": country,
                    "classify": classify,
                    "rating_num": rating_num,
                    "rating_people": rating_people,
                    "quote": quote
                })

            time.sleep(5)

        return movie_list


# ------------------- 单元测试 -------------------
if __name__ == "__main__":
    print(SpiderDoubanMovieTop250().running())
