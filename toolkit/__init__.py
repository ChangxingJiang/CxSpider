# coding=utf-8

import random
from datetime import datetime

from toolkit import file  # [函数组]文件读写相关工具函数
from toolkit.selenium import open_chrome  # [函数]打开Selenium控制的Chrome浏览器
from toolkit.mysql import connect as mysql_connect  # [函数]构造MySQL数据库连接对象


def console(sign: str, sentence: str):
    """
    向控制台输出格式化信息
    格式样例: 2020-06-08 09:09:40 [sign] sentence

    :param sign: <str> 信息标记
    :param sentence: <str> 信息内容
    """
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " [" + sign + "] " + sentence)


def get_scope_random(num, scope=0.2):
    """
    生成散布于期望值附近一定范围内的随机数

    :param num: <float/int> 期望值
    :param scope: <float> 随机范围: 取值范围为[0,1],默认值为0.2(若不再取值范围内则使用默认值)
    """
    if not 0 <= scope <= 1:
        scope = 0.2
    return random.uniform((1 - scope) * float(num), (1 + scope) * float(num))


if __name__ == "__main__":
    pass
