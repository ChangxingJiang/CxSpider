# coding:utf-8


import re
import time

import crawlertool as tool
from Selenium4R import Chrome


class SpiderFacebookAccountInfo(tool.abc.SingleSpider):
    """Facebook账号信息爬虫

    适用于Facebook老版本UI(FB4)的Facebook账号信息爬虫

    @Update 2020.10.22

    有效性检验日期:2020.12.28
    """

    def __init__(self, driver):
        # 爬虫实例的变量
        self.driver = driver
        self.page_url = None

    def running(self, page_url: str):
        """执行Facebook老版UI账号信息爬虫

        :param page_url: Facebook账号主页的Url
        :return: 字典格式的Facebook账号信息数据
        """

        # 初始化爬虫实例的变量
        self.page_url = page_url

        print("开始抓取,目标账号实际请求的Url:", page_url)

        item = {}

        # 执行请求
        self.driver.get(page_url)

        # 等待页面渲染（账号点赞数为Js渲染实现）
        time.sleep(1)

        # 抓取账号唯一ID
        if label := self.driver.find_element_by_css_selector("#entity_sidebar > div:nth-child(1) > div > div > div > a "):
            if pattern := re.search(r"(?<=com/)\d+(?=/)", label.get_attribute('href')):
                item["account_id"] = pattern.group()
        if "account_id" not in item:
            self.log("Facebook账号主页:" + page_url + "|账号唯一ID抓取异常")

        # 抓取账户关注数和点赞数
        if label := self.driver.find_element_by_css_selector("#PagesProfileHomeSecondaryColumnPagelet"):
            if pattern := re.search(r"[\d, ]+(?= 位用户关注了)", label.text):
                item["follow"] = int(pattern.group().replace(",", "").replace(" ", ""))
            else:
                item["follow"] = 0
            if pattern := re.search(r"[\d, ]+(?= 位用户赞了)", label.text):
                item["favor"] = int(pattern.group().replace(",", "").replace(" ", ""))
            else:
                item["favor"] = 0
        else:
            self.log("Facebook账号主页:" + page_url + "|账号关注数和点赞数抓取异常")

        return [item]


# ------------------- 单元测试 -------------------
if __name__ == "__main__":
    driver = Chrome(cache_path=r"E:\Temp")
    print(SpiderFacebookAccountInfo(driver).running("https://www.facebook.com/zaobaosg/"))
    driver.quit()
