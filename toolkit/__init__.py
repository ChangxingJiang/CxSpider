from datetime import datetime

from toolkit.chromedriver import open_chrome  # [函数]打开Selenium控制的Chrome浏览器
from toolkit.mysql import connect as mysql_connect  # [函数]构造MySQL数据库连接对象


def console(sign: str, sentence: str):
    """
    向控制台输出格式化信息
    格式样例: 2020-06-08 09:09:40 [sign] sentence

    :param sign: <str> 信息标记
    :param sentence: <str> 信息内容
    """
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " [" + sign + "] " + sentence)


if __name__ == "__main__":
    pass
