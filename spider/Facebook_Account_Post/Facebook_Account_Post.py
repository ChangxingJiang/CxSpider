# coding:utf-8

import json
import re
import time
from typing import Dict
from typing import List

import crawlertool as tool
from bs4 import BeautifulSoup
from lxml import etree


class SpiderFacebookAccountPost(tool.abc.SingleSpider):
    """Facebook账号推文爬虫"""

    def __init__(self, proxy_port: int = None):
        """构造Facebook推文爬虫实例

        :param proxy_port: 代理端口
        """

        # 请求使用的请求头信息
        self.headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": tool.static.USER_AGENT["Win10_Chrome83"]
        }

        # 请求使用的代理IP地址(可在VPN软件中查询)
        if proxy_port:
            self.proxies = {
                "https": "https://127.0.0.1:{}".format(proxy_port),
                "http": "https://127.0.0.1:{}".format(proxy_port)
            }
        else:
            self.proxies = None

        # 爬虫实例的变量
        self.user_name = None
        self.earliest_post = None

    @staticmethod
    def get_facebook_user_name(page_url: str) -> str:
        """提取Facebook的账号主页名称

        主要用于从Facebook任意账号页的Url中提取Url账号的主页名称

        :param page_url: Facebook任意账号页的Url
        :return: Facebook账号的主页名称
        """
        page_url = re.sub(r"[Hh][Tt][Tt][Pp][Ss]?://[^.]*\.?facebook\.com/p?g?/?", "", page_url)
        return page_url[:page_url.index("/")] if "/" in page_url else page_url

    def running(self, user_name: str, since_timestamp: int, until_timestamp: int) -> List[Dict]:
        """执行Facebook账号推文爬虫

        :param user_name: Facebook账号主页名称（可以通过get_facebook_user_name获取）
        :param since_timestamp: 抓取时间范围的左侧边界（最早时间戳）
        :param until_timestamp: 抓取时间范围的右侧边界（最晚时间戳）
        :return: 推文信息列表
        """

        # 初始化爬虫实例的变量
        self.user_name = user_name  # 记录当前正在抓取的Facebook账号
        self.earliest_post = None  # 时间戳格式的追溯最早推文时间

        post_list = []  # 推文列表
        is_first_page = True  # 是否正在处理账号首页
        timeline_cursor = None  # 下一次请求的Url参数
        user_page_id = None  # 下一次请求的Url参数

        # 计算Facebook账号帖子页的Url
        page_url = "https://www.facebook.com/pg/{}/posts/".format(user_name)

        self.console("开始抓取,目标账号帖子页Url:" + page_url)

        for page in range(200):
            # 处理帖子首页的情况
            if is_first_page:
                # 请求目标Facebook账号的帖子页
                response_text = tool.try_request(url=page_url, headers=self.headers, proxies=self.proxies).content.decode("UTF-8")
                if not response_text:
                    self.log("抓取结束:帖子首页请求结果为空(账号不存在/账号已失效)")
                    return post_list

                # 读取用户的page_id（用作Ajax的请求参数）
                if pattern := re.search(r"(?<=page_id=)\d+(?=&)", response_text):
                    user_page_id = pattern.group()
                else:
                    self.log("抓取结束:读取Facebook账号的page_id失败(账号不存在/账号已失效)")
                    return post_list

                # 解析目标Facebook账号的帖子页:生成etree解析器
                parser = etree.HTML(response_text)

                # 解析目标Facebook账号的帖子页:获取包含反馈数据的Json格式数据
                feedback_json = None
                soup = BeautifulSoup(response_text, "lxml")
                if label := soup.select_one("body > script:nth-child(4)"):
                    if pattern := re.search(r"{.*}", str(label)):
                        try:
                            feedback_json = self.extract_feedback(json.loads(pattern.group())["pre_display_requires"])
                        except (json.JSONDecodeError, KeyError):
                            pass
                if not feedback_json:
                    self.log("抓取结束:帖子首页内容格式异常(出现异常/账号没有发布过帖子)")
                    return post_list

            # 处理非帖子首页的情况（使用Ajax请求获取的下拉页面）
            else:
                self.console("第{}次下拉,当前追溯时间:{}".format(page, self.earliest_post_time))

                # 检查Ajax请求所需参数是否正常
                if not timeline_cursor or not user_page_id:
                    self.log("抓取结束:Ajax请求参数未能正常获取(timeline_cursor/user_page_id为空)")
                    return post_list

                # 计算需要请求的Ajax地址并执行请求
                ajax_url = self.make_ajax_url(timeline_cursor=timeline_cursor, user_page_id=user_page_id)
                response_text = tool.try_request(url=ajax_url, headers=self.headers, proxies=self.proxies).content.decode("UTF-8")
                if not response_text:
                    self.log("抓取结束:Ajax请求结果为空(出现异常/已抓取该账号的所有推文)")
                    return post_list

                # 解析Ajax请求结果
                parser, feedback_json = None, None
                if pattern := re.search(r"{.*}", response_text):
                    try:
                        response_json = json.loads(pattern.group())
                        parser = etree.HTML(response_json["domops"][0][3]["__html"])
                        feedback_json = self.extract_feedback(response_json["jsmods"]["pre_display_requires"])
                    except (json.JSONDecodeError, KeyError):
                        pass
                if parser is None or feedback_json is None:
                    self.log("抓取结束:帖子的Ajax加载内容格式异常(出现异常/账号没有发布过帖子)")
                    return post_list

            # 遍历解析请求的推文
            for post_node in self.parse_post_nodes(parser, is_first_page):
                # 解析当前推文信息
                item = self.parse_post(post_node=post_node, feedback_json=feedback_json)

                # 依据推文的发布时间具体进行处理
                if "tweet_timestamp" not in item or item["tweet_timestamp"] > until_timestamp:
                    # 如果当前推文晚于抓取时间范围的右侧边界则跳过当前推文
                    continue
                elif until_timestamp >= item["tweet_timestamp"] > since_timestamp:
                    # 如果当前推文处于抓取时间范围内则存储当前推文
                    post_list.append(item)
                elif not item["if_sticky"]:
                    # 如果当前推文早于抓取时间范围的左侧边界且不是置顶推文则结束当前抓取
                    self.log("抓取完成:目标时间段的推文已抓取完成,当前追溯时间:{}".format(self.earliest_post_time))
                    return post_list

            # 解析下一次url的timeline_cursor参数
            timeline_cursor = self.parse_timeline_cursor(parser)
            if not timeline_cursor:
                self.log("抓取完成:已没有继续下拉的timeline_cursor(已抓取该账号的所有推文)")
                return post_list

            is_first_page = False

            time.sleep(3)

        self.log("抓取结束:已经连续下拉达到200次")
        return post_list

    @staticmethod
    def make_ajax_url(user_page_id: str, timeline_cursor: str) -> str:
        """生成Ajax请求的Url

        :param user_page_id Ajax的请求参数，用于控制帖子的发布者
        :param timeline_cursor Ajax的请求参数，用于控制帖子的发布时间范围
        """
        cursor = "%7B%22timeline_cursor{}timeline_section_cursor%22%3A%7B%7D%2C%22has_next_page%22%3Atrue%7D"
        request_param = ("page_id=" + user_page_id +
                         "&cursor=" + cursor.format(timeline_cursor) +
                         "&surface=www_pages_posts" +
                         "&unit_count=8" +
                         "&fb_dtsg_ag=AQy5MmV05j9OTQTX_onghnrR-4JxA_UzSqa0P9rXKb8TSA:AQytUGwqgDUMC9nTbJX3LlUhJupCRU_s3VNsmt47p8p-_Q" +
                         "&__dyn=7AgNeS4amaAxd2u6aJGeFxqeCwKyaGey8gF4Wo8oeES2N6wAxubwTwFwMzFUKbnyorxuF8vDK7HzEeWDwUz8S2SVFEgU9A69V8KUO5UlwQxS58iwBx61cxq2e1tG7ElwupVk2u2-262O4rG7ooxu6U9GwgEdoKfzUaU-1dx3ximfKEgzU6a48y4EhwG-Ury9m4-2ei48-cBKm4U-5898Gfxm3ibxuE4ah4Bx3CDKi8wGxm4UGqfwhUO68gy8y6Ue8Wqexp2Utwwx-2y8xa489o4-262O2WE9EjwtUym2mfxW68lBw" +
                         "&__user=0" +
                         "&__a=1" +
                         "&__be=1" +
                         "&__pc=PHASED%3ADEFAULT" +
                         "&dpr=1" +
                         "&__rev=1001437401")
        return "https://www.facebook.com/pages_reaction_units/more/" + "?" + request_param

    @staticmethod
    def parse_timeline_cursor(parser: "etree.Element") -> str:
        """解析下一次请求的timeline_cursor参数

        :param parser: etree的HTML解析器
        :return: 下一次请求的timeline_cursor参数
        """
        if ajax_timeline := parser.xpath("//a[@class='pam uiBoxLightblue uiMorePagerPrimary']/@ajaxify"):
            if pattern := re.search("(?<=timeline_cursor).*(?=timeline_section_cursor)", ajax_timeline[0]):
                return pattern.group()

    @staticmethod
    def extract_feedback(feedback_source_list: List) -> Dict:
        """提取推文反馈数据

        :param feedback_source_list: 包含反馈数据的Json格式源数据
        :return: 提取后的包含反馈数据的Json格式数据
        """
        feedback_json = {}
        for feedback_source_item in feedback_source_list:
            try:
                if feedback_source_item[0] == "RelayPrefetchedStreamCache":
                    feedback_item = feedback_source_item[3][1]["__bbox"]["result"]["data"]["feedback"]
                    feedback_json[feedback_item["subscription_target_id"]] = feedback_item
            except TypeError:
                continue
        return feedback_json

    @staticmethod
    def parse_post_nodes(parser: "etree.Element", is_first_page: bool) -> List["etree.Element"]:
        """解析当前请求的推文最外层节点列表

        :param parser: etree的HTML解析器
        :param is_first_page: 是否正在处理账号首页
        :return: 推文的最外层节点列表
        """
        if is_first_page:  # 处理账号首页的情况
            return parser.xpath("//div[@id='pagelet_timeline_main_column']//div[@class='_4-u2 _4-u8']")
        else:  # 处理Ajax请求结果的情况
            return parser.xpath("//div[@class='_4-u2 _4-u8']")

    def parse_post(self, post_node: "etree.Element", feedback_json: Dict) -> Dict:
        """解析推文信息

        :param post_node: 推文的最外层节点
        :param feedback_json: 包含反馈数据的Json格式数据
        :return: 包含推文信息的Json格式数据
        """
        item = {"if_share": False}

        # 重新以当前节点为最上层节点解析DOM结构
        post_node = etree.HTML(etree.tostring(post_node))

        # 解析推文是否为置顶推文
        item["if_sticky"] = "置顶帖" in post_node.xpath("//div[@class='_5pcr userContentWrapper']//i/@data-tooltip-content")

        # 解析推文的发布者
        if result := post_node.xpath("//div[@class ='_6a _5u5j']//span[contains(@class,'fwb')]/a/text()"):
            item["author"] = result[0]

        # 解析推文的ID
        if result := post_node.xpath("//div[@class='_6a _5u5j']//div[@class='_5pcp _5lel _2jyu _232_']/@id"):
            if pattern := re.search(r"(?<=[;:])\d{2,}", result[0]):
                item["tweet_id"] = pattern.group()

        # 解析推文的发布时间
        if result := post_node.xpath("//span[@class='fsm fwn fcg']//abbr/@data-utime"):
            if pattern := re.search(r"\d+", result[0]):
                item["tweet_timestamp"] = int(pattern.group())
                item["tweet_date"], item["tweet_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item["tweet_timestamp"])).split(" ")

                # 更新追溯最早推文时间
                if not item["if_sticky"] and (not self.earliest_post or self.earliest_post > item["tweet_timestamp"]):
                    self.earliest_post = item["tweet_timestamp"]

        # 解析推文配图的Url
        if result := post_node.xpath("//div[@class='_6l- __c_']/div/img/@src"):
            item["img_url"] = result[0]

        # 解析推文内容
        if result := post_node.xpath("//div[@class='_5pbx userContent _3576']//text()"):
            item["text"] = " ".join(result)

        # 解析提取后的推文反馈数据
        if "tweet_id" in item and item["tweet_id"] in feedback_json:
            feedback_item = feedback_json[item["tweet_id"]]
            try:
                item["tweet_url"] = feedback_item["url"]
                item["reaction"] = feedback_item["reaction_count"]["count"]
                item["comment"] = feedback_item["comment_count"]["total_count"]
                item["share"] = feedback_item["share_count"]["count"]
            except TypeError:
                self.console("推文反馈Json数据中没有推文ID(推文反馈数据格式异常)")
        else:
            self.console("推文反馈Json数据中没有推文ID(可能为直播)" + str(item.get("tweet_id")))

        return item

    @property
    def earliest_post_time(self) -> str:
        """返回文本格式的追溯最早推文时间"""
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.earliest_post))


# ------------------- 单元测试 -------------------
if __name__ == "__main__":
    print(SpiderFacebookAccountPost().running(
        user_name=SpiderFacebookAccountPost.get_facebook_user_name("https://www.facebook.com/zaobaosg/"),
        since_timestamp=int(time.mktime(time.strptime("2020-12-01", "%Y-%m-%d"))),
        until_timestamp=int(time.mktime(time.strptime("2020-12-20", "%Y-%m-%d")))
    ))
