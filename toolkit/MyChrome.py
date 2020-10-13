"""
Selenium工具类
"""

import os
import time

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

import environment as env


class MyChrome(WebDriver):
    """
    Chrome浏览器驱动类

    增加了自动读取环境变量的功能
    """

    def __init__(self, executable_path="chromedriver", port=0,
                 options=None, service_args=None,
                 desired_capabilities=None, service_log_path=None,
                 chrome_options=None, keep_alive=True, use_user_dir: bool = True):
        """
        创建Chrome浏览器驱动实例

        启动服务，然后创建一个新的Chrome浏览器驱动实例

        原生参数：
        :param executable_path: Chrome浏览器的可执行文件路径 (默认 = $PATH中的chromedriver变量)
        :param port: Chrome浏览器运行的端口我 (默认 = 自动寻找一个空闲端口)
        :param options: ChromeOptions (设置参数实例)
        :param service_args: 服务参数
        :param desired_capabilities: 非浏览器功能设置
        :param service_log_path: Chrome浏览器服务日志路径
        :param chrome_options: 已弃用的设置参数实例
        :param keep_alive: 是否将ChromeRemoteConnection设置为 "HTTP keep-alive"

        用户参数：
        :param use_user_dir: <bool> 是否使用本地Chrome浏览器中已登录的Google账号 (默认=True)
        """

        # 设置executable_path参数
        if executable_path not in os.environ:
            executable_path = env.CHROMEDRIVER_PATH

        # 设置options参数 (设置参数实例)
        if not options:
            options = Options()  # 构造Selenium控制的Chrome浏览器的设置对象

        if use_user_dir:
            options.add_argument("user-data-dir=" + env.CHROME_USERDATA_PATH)  # 设置Chrome浏览器的Google账号用户文件地址

        # options.binary_location = env.CHROME_LOCATION  # 设置Chrome浏览器的可执行文件地址(如果Chrome浏览器启动个报错则启动本行)

        options.add_experimental_option("prefs", {
            "download.default_directory": env.CHROME_DOWNLOAD_PATH,  # 设置Chrome浏览器下载文件的存储路径
            "download.prompt_for_download": False,  # 设置Chrome浏览器下载文件是否弹出窗口
        })

        # 启动Selenium控制的Chrome浏览器
        super().__init__(executable_path=executable_path, port=port,
                         options=options, service_args=service_args,
                         desired_capabilities=desired_capabilities, service_log_path=service_log_path,
                         chrome_options=chrome_options, keep_alive=keep_alive)

    def load_jquery(self):
        """
        在当前页面中加载JQuery库

        依据本地的JQuery文件，在当前页面中加载JQuery库
        """
        with open("../toolkit/jquery-3.5.1.min.js") as file:
            self.execute_script(file.read())

    def post(self, url, params=None, payload=False):
        """
        执行Post请求

        :param url: 请求的目标Url
        :param params: 请求传参
        :param payload: False为使用FormData传参(默认)，True为使用PayLoad传参
        :return: 请求的返回值
        """
        # 在当前页面中加载JQuery库
        self.load_jquery()

        # 将传参转换为Js对象
        if params:
            self.execute_script("window.req_data = %s;" % str(params))
        else:
            self.execute_script("window.req_data = {};")

        # 生成两种不同的传参方法的Ajax请求的Js代码
        if payload:  # 处理PayLoad传参方法
            js_ajax = "$.ajax('%s',{method:'POST',contentType:'application/json;charset=utf-8',data:JSON.stringify(window.req_data),success:function(res){window.req_res=res}});"
        else:  # 处理FormData传参方法
            js_ajax = "$.ajax('%s',{method:'POST',contentType:'application/x-www-form-urlencoded;charset=UTF-8',data:window.req_data,success:function(res){window.req_res=res}});"
        self.execute_script(js_ajax % url)

        # 等待Ajax请求的时间
        time.sleep(3)

        # 获取Ajax请求的结果
        return self.execute_script("return window.req_res;")


if __name__ == "__main__":
    import json

    selenium = MyChrome(use_user_dir=False)
    selenium.get("https://leetcode-cn.com/problemset/all/")  # 打开题库页面

    # 题目翻译的查询参数(GraphQL接口)
    GRAPHQL_QUERY_TRANSLATIONS = {
        "operationName": "getQuestionTranslation",
        "variables": {},
        "query": "query getQuestionTranslation($lang: String) {\n  translations: allAppliedQuestionTranslations(lang: $lang) {\n    title\n    questionId\n    __typename\n  }\n}\n"
    }

    GRAPHQL_URL = "https://leetcode-cn.com/graphql"

    print(selenium.post(GRAPHQL_URL, json.dumps(GRAPHQL_QUERY_TRANSLATIONS), payload=True))
