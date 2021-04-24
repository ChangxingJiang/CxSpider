"""
LeetCode题目列表爬虫

@author: ChangXing
@version: 1.0
@create: 2020.08.31
@revise: ----.--.--
"""

import json

import requests
from Selenium4R import Chrome

PROBLEMS_SET_URL = "https://leetcode-cn.com/problemset/all/"  # LeetCode网页中“题库”页面的Url
PROBLEMS_ALL_API = "https://leetcode-cn.com/api/problems/all/"  # 读取题目列表的API接口的Url
PROBLEMS_TAGS_API = "https://leetcode-cn.com/problems/api/tags/"  # 读取题目标签的API接口的Url
GRAPHQL_API = "https://leetcode-cn.com/graphql"  # GraphQL查询语言的API接口的Url

# 题目翻译的API接口查询参数(GraphQL接口)
GRAPHQL_QUERY_TRANSLATIONS = {
    "operationName": "getQuestionTranslation",
    "variables": {},
    "query": "query getQuestionTranslation($lang: String) {\n  translations: allAppliedQuestionTranslations(lang: $lang) {\n    title\n    questionId\n    __typename\n  }\n}\n"
}


class Problem:
    __slots__ = ["id", "front_id", "slug", "title", "acs", "submit", "articles", "level", "paid_only", "tags"]

    def __init__(self, elem):
        """生成题目实例"""
        self.id = elem["stat"]["question_id"]  # 题目ID = LeetCode内置的题目ID（对外没有显示）
        self.front_id = elem["stat"]["frontend_question_id"]  # 题目显示ID = LeetCode用于页面显示的题目ID
        self.slug = elem["stat"]["question__title_slug"]  # 题目地址 = LeetCode题目地址（题目Url：https://leetcode-cn.com/problems/%s/）
        self.title = elem["stat"]["question__title"]  # 题目中文名 = LeetCode对外显示的题目中文名
        self.acs = elem["stat"]["total_acs"]  # 题目累计通过次数
        self.submit = elem["stat"]["total_submitted"]  # 题目累计提交次数
        self.articles = elem["stat"]["total_column_articles"]  # 题目题解数量
        self.level = ["简单", "中等", "困难"][elem["difficulty"]["level"] - 1]  # 题目难度：1=简单；2=中等；3=困难
        self.paid_only = "会员" if elem["paid_only"] else "免费"  # 题目是否仅会员可用
        self.tags = []  # 题目标签列表

    def add_tag(self, tag):
        """添加题目标签"""
        self.tags.append(tag)

    def get_lst(self):
        """生成数据列表"""
        lst = [self.id, self.front_id, self.slug, self.title, self.acs, self.submit, self.articles, self.level, self.paid_only, " ".join(self.tags)]
        return [str(elem) for elem in lst]


def crawler(file_name):
    """
    LeetCode题目列表爬虫

    :param file_name: 抓取结果存储文件地址
    """
    selenium = Chrome(cache_path=r"E:\Temp")  # 启动Chrome浏览器驱动
    selenium.get(PROBLEMS_SET_URL)  # 打开题库页面

    # 获取题目列表(Json格式)
    problems_all_json = requests.get(PROBLEMS_ALL_API).json()
    print("解析题目总数:", problems_all_json["num_total"])

    # 解析题目列表(生成problem实例列表):key=题目ID,value=题目的problem实例
    result_problems = {}
    for problem in problems_all_json["stat_status_pairs"]:
        problem_elem = Problem(problem)
        result_problems[problem_elem.id] = problem_elem

    # 获取题目标签(Json格式)并将结果写入到题目列表中
    problems_tags_json = requests.get(PROBLEMS_TAGS_API).json()
    for topic in problems_tags_json["topics"]:
        tag_name = topic["translatedName"] if topic["translatedName"] else topic["name"]
        for qid in topic["questions"]:
            if qid in result_problems:
                result_problems[qid].add_tag(tag_name)
            else:
                print("题目ID未找到:", qid, tag_name)

    # 获取题目翻译(Json格式)并将结果写入到题目列表中
    translations_json = selenium.post(GRAPHQL_API, json.dumps(GRAPHQL_QUERY_TRANSLATIONS), payload=True)
    for problem in translations_json["data"]["translations"]:
        if (qid := int(problem["questionId"])) in result_problems:
            result_problems[qid].title = problem["title"]

    # 管理Chrome浏览器驱动
    selenium.quit()

    # 排序题目列表(依据题目显示ID排序)
    problem_keys = list(result_problems.keys())
    problem_keys.sort(key=lambda x: (int(front_id) if (front_id := result_problems[x].front_id).isdigit() else float("inf"), front_id))

    # 生成最终结果列表(数据列表)
    result_data = "\n".join([",".join(result_problems[pid].get_lst()) for pid in problem_keys])

    # 将结果写入到csv文件中
    with open(file_name, encoding="ANSI", mode="w", errors="ignore") as file:
        file.write(result_data)


if __name__ == "__main__":
    crawler(r"C:\Users\Changxing\Desktop\LeetCode题目列表_20210423.csv")
