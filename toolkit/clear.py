import re


def invisible(text: str):
    """
    清除不可见字符
    包括：制表符、回车符、换行符、全半角空格

    :param text: <str> 需要清洗的字符串
    :return <str> 清洗完成的字符串
    """
    return re.sub("[\t\r\n 　]", "", text)


if __name__ == "__main__":
    pass