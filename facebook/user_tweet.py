"""
Facebook推文爬虫

@author: ChangXing
@version: 4.1
@create: 2017.12.30
@revise: 2020.06.09
"""

import copy
import json
import re
import time

import requests
from bs4 import BeautifulSoup
from requests.exceptions import ProxyError
from urllib3.exceptions import MaxRetryError

from toolkit import environment as env

import Utils4R as Utils


def crawler(posts_url, time_start, time_end, template):
    """ 抓取Facebook用户指定时间范围内的所有推文
    :param posts_url: <str> Facebook用户帖子页Url
    :param time_start: <int> 时间范围开始时间戳
    :param time_end: <int> 时间范围结束时间戳
    :return: <list:crawler.item.Item> Facebook推文的Item对象列表
    """
    tweet_list = []  # Facebook推文的Item对象列表
    ajax_url = None  # [数据] 提取Ajax请求的Url

    for i in range(200):  # 最多对每个账号执行200次请求(大概最多1600条推文)
        if i == 0:  # 第一次请求Facebook用户帖子页
            try:
                response = requests.get(posts_url, proxies=env.VPN_PROXY)
            except OSError or ConnectionResetError or ProxyError or MaxRetryError:
                Utils.console("报错", "请求失败,网络可能出现问题,请检查")
                return tweet_list
            if response:
                bs = BeautifulSoup(response.content.decode(errors="ignore"), 'lxml')  # 将帖子页HTML转换为BeautifulSoup对象
                feedback_dict = parser_feedback_json(locate_feedback_json(bs))  # [数据] 提取推文反馈数据所在Json数据 + 解析推文反馈数据
                label_list = bs.select("#pagelet_timeline_main_column > div > div:nth-child(2) > div > div._4-u2._4-u8")
            else:
                return tweet_list
        else:  # 后续的请求请求
            if ajax_url is None:
                Utils.console("报错", "Ajax的Url为空，结束当前用户的抓取")
                return tweet_list
            try:
                response = requests.get(ajax_url, proxies=env.VPN_PROXY)  # 请求Facebook用户Ajax更新页
            except OSError or ConnectionResetError or ProxyError or MaxRetryError:
                Utils.console("报错", "请求失败,尝试等待20秒后重新请求")
                time.sleep(20)
                try:
                    response = requests.get(ajax_url, proxies=env.VPN_PROXY)  # 请求Facebook用户Ajax更新页
                except OSError or ConnectionResetError or ProxyError or MaxRetryError:
                    Utils.console("报错", "尝试等待20秒后请求再次失败,放弃当前媒体抓取")
                    return tweet_list
            if response:
                ajax_json = json.loads(response.content.decode(errors="ignore").replace("for (;;);", ""))
                if ajax_json is not None:
                    bs = BeautifulSoup(ajax_json["domops"][0][3]["__html"])  # 将HTML部分转换为BeautifulSoup对象
                    feedback_dict = parser_feedback_json(ajax_json["jsmods"])  # [数据] 解析推文反馈数据
                    label_list = bs.select("div._1xnd > div._4-u2._4-u8")  # [定位] 定位到推文标签列表
                else:
                    return tweet_list
            else:
                return tweet_list

        Utils.console("运行", "执行第" + str(i + 1) + "次请求,返回数量: " + str(len(label_list)))

        # 解析推文标签数据
        for label in label_list:  # 遍历推文标签列表
            tweet_info = parser_tweet(label, feedback_dict, template)  # 解析推文标签中所有内容并返回推文的Item对象
            if tweet_info is None:
                continue
            if tweet_info["time"] == 0:  # 若推文时间抓取失败则跳过当前推文
                continue
            elif tweet_info["time"] > time_end:  # 推文晚于抓取时间范围结束时间的情况(跳过当前推文)
                continue
            elif tweet_info["time"] >= time_start:  # 推文处于抓取时间范围的情况(保存当前推文)
                tweet_list.append(tweet_info)  # [数据] 解析推文标签中所有内容并返回推文的Item对象
            else:  # 推文早于抓取时间范围开始时间的情况(跳出当前用户)
                if not tweet_info["is_sticky"]:
                    return tweet_list

        ajax_url = get_ajax_href(bs)  # [数据] 提取Ajax请求的Url
        time.sleep(3)  # 延时3秒

    return tweet_list


def get_facebook_user_name(url):
    """
    通过Facebook用户主页Url，计算Facebook用户主页名称

    :param url: <str> Facebook用户主页Url
    :return: <str> Facebook用户主页名称
    """
    name = url.replace("zh-cn.", "").replace("www.", "").replace("m.", "").replace("https://facebook.com/", "")
    if "id" not in name:  # 不清除包含id的参数,形如: https://www.facebook.com/profile.php?id=100005497590742
        name = re.sub(r"\?.*$", "", name)  # 清除url参数中的内容
    return re.sub("/$", "", name)


def parser_tweet(label, feedback_dict, template):
    """ [数据] 解析推文标签中所有内容并返回推文的Item对象
    :param label: <bs4.element.Tag> 推文标签：<div._4-u2._4-u8>
    :param feedback_dict: <dict:str-dict> 推文反馈数据对应表
    :param template: None
    :return: <crawler.item.Item> Facebook推文的Item对象
    """
    item = copy.deepcopy(template)  # 构造Facebook推文的Item对象
    label_wrapper = label.select_one("div._4-u2._4-u8 > div > div > div > div.userContentWrapper")  # 定位到推文外层标签(第2层)
    if label_wrapper is None:
        Utils.console("报错", "推文外层标签定位失败,放弃当前推文抓取")
        return None
    label_main = locate_main_label(label_wrapper, item)  # [定位] 定位到推文标题标签(第3层) + [数据] 提取推文正文标签中的数据：推文是否置顶
    if label_main is not None:
        label_title = locate_title_label(label_main)  # [定位] 定位到推文标题标签(第4层)
        get_from_title(label_title, item)  # [数据] 提取推文标签标题中的数据：包括推文ID、推文Url、推文是否为分享、推文发布者、推文发布时间
        label_content = label_main.select_one("div." + label_main["class"] + ' > div:nth-child(2)')  # 定位到推文内容标签(第4层)
        item["content"] = label_content.text  # [数据] 提取推文内容标签中的数据：推文内容
        if item["tweet_id"] is None:
            search_tweet_id(label_wrapper, item)  # [数据] 再次提取：推文ID
        get_from_feedback(feedback_dict, item)  # [数据] 提取推文反馈Json数据中的数据：包括推文Url、推文点赞数、推文评论数、推文转发数、推文视频播放数
        return item
    else:
        print("解析推文对象异常!")
        return None


def get_ajax_href(soup):
    """ [数据] 提取Ajax请求的Url
    :param soup: <bs4.BeautifulSoup> / <bs4.element.Tag> 包含Ajax请求Url所在标签的BeautifulSoup对象或Tag对象
    :return: <str> Ajax请求Url / <None> 不包含
    """
    # [定位] 定位到Ajax请求Url所在标签(第2层)
    label = soup.select_one("#www_pages_reaction_see_more_unitwww_pages_posts > div > a")

    # [数据] 提取：Ajax请求Url所在的ajaxify属性
    ajax_href = label["ajaxify"]  # 读取Ajax请求Url所在属性
    if ajax_href.is_empty():
        Utils.console("报错", "获取Ajax请求的Url失败:" + str(label))
        return None

    # [数据] 处理：依据ajaxify属性计算Ajax请求的Url
    other_param = "&fb_dtsg_ag&__user=0&__a=1&__csr=&__req=c&__be=1&__pc=PHASED%3ADEFAULT&dpr=1&__rev=1001280609"
    return "https://www.facebook.com" + str(ajax_href) + other_param


def locate_main_label(wrapper_label, item):
    """ [定位] 定位到推文正文标签(第3层) + [数据] 提取推文正文标签中的数据：推文是否置顶
    :param wrapper_label: <bs4.element.Tag> 推文外层标签
    :param item: <crawler.item.Item> Facebook推文的Item对象
    :return: <bs4.element.Tag> 推文正文标签
    """
    # [数据] 提取：推文是否置顶
    selector_sticky = "div.userContentWrapper > div:nth-child(1) > div"
    if len(wrapper_label.select(selector_sticky)) == 3:  # 判断推文是否为置顶
        item["is_sticky"] = True
        selector = "div.userContentWrapper > div:nth-child(1) > div:nth-child(3)"  # > div:nth-child(1)
    else:
        selector = "div.userContentWrapper > div:nth-child(1) > div:nth-child(2)"

    # [定位] 定位到推文正文标签(第3层)
    main_label = wrapper_label.select_one(selector)
    if main_label is not None:
        main_label["class"] = "mark_main_label"
    else:
        print("定位推文正文标签出现异常!")
        return None
    return main_label


def locate_title_label(main_label):
    """ [定位] 定位到推文标题标签(第4层)
    :param main_label: <bs4.element.Tag> 推文正文标签
    :return: <bs4.element.Tag> 推文标题标签：class="_6a _5u5j _6b",children=[h5,div]
    """
    main_class = main_label["class"]  # 获取推文正文标签的class属性用于定位
    selector = "div.{}> div:nth-child(1) > div > div:nth-child(2) > div:nth-child(2) > div > div > div:nth-child(2)"
    return main_label.select_one(selector.format(main_class))


def get_from_title(title_label, item):
    """ [数据] 提取推文标签标题中的数据：包括推文ID、推文Url、推文是否为分享、推文发布者、推文发布时间
    :param title_label: <bs4.element.Tag> 推文标题标签
    :param item: <crawler.item.Item> Facebook推文的Item对象
    :return: <None> 更新结果于Facebook推文的Item对象
    """
    title_class = title_label["class"]  # 获取推文标签标题的class属性用于定位

    # [数据] 提取：推文ID
    selector_tweet_id = "div." + title_class + " > div"
    tweet_id_source = title_label.select_one(selector_tweet_id)["id"]  # 提取推文ID
    if re.search("(?<=;)[0-9]+(?=;;)", tweet_id_source):
        item["tweet_id"] = re.search("(?<=;)[0-9]+(?=;;)", tweet_id_source).group()  # 整理推文ID（提取其中数字部分）

    # [数据] 提取：推文发布者
    selector_author = "div." + title_class + " > h5"
    author = title_label.select_one(selector_author).text  # 提取推文发布者

    # [数据] 提取：推文发布时间
    selector_time = "div." + title_class + " > div > span > span > a > abbr"
    item["time"] = int(title_label.select_one(selector_time)["data-utime"])  # 提取推文发布时间戳

    # [数据] 计算：推文是否为分享
    if "分享" in author:  # 判断推文是否为分享
        item["is_share"] = True
        # 读取分享推文的推文发布者
        selector_author = "div." + title_class + " > h5 > span > span > a"
        author_source = title_label.select_one(selector_author)["href"]  # 推文发布者名称所在属性
        if "直播视频" in author:  # 如果转载内容包括"直播视频",则推文发布者为直播视频
            item["author"] = "[直播视频]"
        elif author_source is not None:  # 判断是否提取到分享来源用户
            if re.search("(?<=^/)[^/]+", author_source) is not None:  # 在发布者名称所在属性中检索发布者的主页名称
                item["author"] = re.search("(?<=^/)[^/]+", author_source).group()
            else:
                Utils.console("警告", "转发推文来源可能不是Facebook用户:" + author)
    else:
        item["author"] = author  # 若推文不是分享，则填写推文发布者


def search_tweet_id(label_wrapper, item):
    """ [数据] 再次提取：推文ID
    :param label_wrapper: <bs4.element.Tag> 推文外层标签
    :param item: <crawler.item.Item> Facebook推文的Item对象
    :return: <None> 更新结果于Facebook推文的Item对象
    """
    selector = "div.userContentWrapper > div:nth-child(2) > form > input:nth-child(3)"
    if tweet_id := label_wrapper.select_onr(selector)["value"]:  # 提取反馈数据部分包含的推文ID
        item["tweet_id"] = str(tweet_id)


def locate_feedback_json(soup):
    """ [数据] 提取推文反馈数据所在Json数据
    :param soup: <bs4.BeautifulSoup> 网页的BeautifulSoup对象
    :return: <dict> 推文反馈数据所在Json数据
    """
    selector = "body > script:nth-child(4)"
    feedback_text = soup.select_one(selector).text  # 提取推文反馈数据所在Json文件所在script标签内容
    feedback_text = re.sub(r"^new \(require\(\"ServerJS\"\)\)\(\).handle\(", "", feedback_text)
    feedback_text = re.sub(r"\);$", "", feedback_text)
    return json.dumps(feedback_text)


def parser_feedback_json(feedback_json):
    """ [数据] 解析推文反馈数据
    :param feedback_json: <dict> 推文反馈数据所在Json数据
    :return: <dict:str-dict> 推文反馈数据对应表(key=推文ID,value=推文ID对应的推文反馈Json数据) / <None> 推文反馈数据所在Json数据异常
    """
    if feedback_json is None:
        Utils.console("报错", "推文反馈数据的Json格式异常,怀疑用户类型错误")
        return None

    if "pre_display_requires" not in feedback_json:
        Utils.console("报错", "推文反馈数据的Json中未找到pre_display_requires属性")
        return None

    feedback_dict = {}  # 定义推文反馈数据对应表
    len(feedback_json["pre_display_requires"])
    for item_list in feedback_json["pre_display_requires"]:
        if not isinstance(item_list, list) or len(item_list) == 0:
            continue
        if item_list[0] == "RelayPrefetchedStreamCache":
            feedback_item = item_list[3][1]["__bbox"]  # 读取推文反馈Json数据
            tweet_id = feedback_item["result"]["data"]["feedback"]["subscription_target_id"]  # 读取推文ID
            feedback_dict[tweet_id] = feedback_item

    return feedback_dict


def get_from_feedback(feedback_dict, item):
    """ [数据] 提取推文反馈Json数据中的数据：包括推文Url、推文点赞数、推文评论数、推文转发数、推文视频播放数
    :param feedback_dict: <dict:str-dict> 推文反馈数据对应表
    :param item: <crawler.item.Item> Facebook推文的Item对象
    :return: <None> 更新结果于Facebook推文的Item对象
    """
    if item.get("tweet_id") is None or item.get("tweet_id") not in feedback_dict:
        Utils.console("报错", "未能在推文反馈Json数据中找到的推文ID:" + str(item.get("tweet_id")))
        return None
    feedback_item = feedback_dict[item.get("tweet_id")]
    item["tweet_url"] = feedback_item["result"]["data"]["feedback"]["url"]  # 提取：推文Url
    item["reaction"] = feedback_item["result"]["data"]["feedback"]["reaction_count"]["count"]  # 提取：推文点赞总数
    item["comment"] = feedback_item["result"]["data"]["feedback"]["comment_count"]["total_count"]  # 提取：推文评论总数
    item["share"] = feedback_item["result"]["data"]["feedback"]["share_count"]["count"]  # 提取：推文分享总数


if __name__ == "__main__":
    mysql_catalogue = tool.mysql_connect("Huabang(old)")  # 构造MySQL数据库连接对象
    mysql_saving = tool.mysql_connect("Huabang")  # 构造MySQL数据库连接对象

    time_start = int(time.mktime(time.strptime("2020-01-29 00:00:00", "%Y-%m-%d %H:%M:%S")))  # 开始时间
    time_end = int(time.mktime(time.strptime("2020-01-29 23:59:59", "%Y-%m-%d %H:%M:%S")))  # 结束时间

    # 读取榜单媒体名录中的Facebook账号Url列表
    media_list = mysql_catalogue.select("media_list", ["media_id", "media_name", "media_fb"])

    for media in media_list:
        # 判断媒体是否有Facebook用户主页Url
        if media[2] is None or media[2] == "" or media[2] == "None":
            continue

        # 判断媒体主页是否存在异常(或需要登录无法抓取)
        if media[0] in [16, 38, 46, 189, 229, 244, 249, 296, 310, 332, 338, 344, 390, 435, 471, 472, 538, 552, 577]:
            Utils.console("报错", media[1] + "(" + str(media[0]) + ")为页面异常媒体，已跳过该媒体")
            continue

        facebook_name = get_facebook_user_name(media[2])  # 依据Facebook用户主页Url计算用户名称
        posts_url = "https://www.facebook.com/pg/{}/posts/?ref=page_internal".format(facebook_name)  # 依据用户名称计算用户帖子页Url

        Utils.console("运行", "开始抓取媒体:" + media[1] + "(" + str(media[0]) + ")")

        template = {
            "media_id": media[0],  # 媒体ID
            "media_name": media[1],  # 媒体ID
            "cr_month": 2006,  # 抓取所属时间范围
            "tweet_id": None,  # 推文ID
            "tweet_url": None,  # 推文Url
            "is_sticky": False,  # 推文是否置顶
            "is_share": False,  # 推文是否为分享
            "author": None,  # 推文发布者
            "time": None,  # 推文发布时间戳(单位:秒)
            "content": None,  # 推文内容
            "reaction": None,  # 推文互动数(前点赞数)
            "comment": None,  # 推文评论数
            "share": None  # 推文分享
        }
        tweet_list = crawler(posts_url, time_start, time_end, template)  # 抓取Facebook用户指定时间范围内的所有推文
        write_num = mysql_saving.insert_pure("facebook_tweet_2020", tweet_list)

        Utils.console("运行", "抓取完成媒体:" + media[1] + "(" + str(media[0]) + ");累计抓取记录数:" + str(write_num))
        time.sleep(5)
