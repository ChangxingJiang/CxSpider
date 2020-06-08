# coding=utf-8

"""
代理IP相关工具类
"""

import json
import random
import time

import requests

import environment as env


class ProxyIP:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = int(port)
        self.request_num = 0
        self.start_time = time.time()
        print("请求获取代理IP | " + str(self))

    def __str__(self):
        return str(self.ip) + ":" + str(self.port)

    def proxy(self):
        self.request_num += 1  # 代理IP使用计数
        return {"http": str(self), "https": str(self)}

    def remove(self):
        print("移除失效代理IP | " + str(self),
              "请求次数=" + str(self.request_num), "有效时长:", round(time.time() - self.start_time))


class Proxy:
    def __init__(self, size: int = 3):
        """
        代理IP管理器

        :param size: <int> 代理IP池容量
        """
        self.size = size
        self.pool = []  # 初始化线程池对象
        self.load(size)  # 获取代理IP充满线程池

    def get(self, num=None):
        if self.size == 0:
            return None
        if num is None or num < 0 or num >= self.size:
            num = random.randint(0, len(self.pool) - 1)
        self.pool[num]["request_num"] += 1
        return self.pool[num].proxy()

    def remove(self, ip_str):
        ip, port = ip_str.split(":")
        delete = None
        for item in self.pool:
            if ip == item.ip and int(port) == item.port:
                delete = item
        if delete is not None:
            delete.remove()
            self.pool.remove(delete)
            if len(self.pool) < self.size:  # 加载新的代理IP
                self.load(self.size - len(self.pool))

    def load(self, num):
        if num > 0:
            response = requests.get(env.PROXY_API.format(num))
            proxy_json = json.loads(response.content.decode(errors="ignore"))
            if proxy_json is None or proxy_json["code"] != 200:
                print("代理IP请求失败:" + str(proxy_json))
            else:
                for data in proxy_json["data"]:
                    if "ip" not in data or "port" not in data:
                        print("调取代理IP失败: " + str(data))
                    self.pool.append(ProxyIP(data["ip"], data["port"]))

    def __str__(self):
        return str({
            "size": self.size
        })
