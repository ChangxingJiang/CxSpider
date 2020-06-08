import re


def number(text: str):
    """
    提取字符串中的数字

    可以提取的数字格式(优先级从高到低)：
    [0-9,.]+(?=亿)
    [0-9,.]+(?=万)
    [0-9,]+
    [0-9,.]+

    :param text: <str> 需要提取数字的字符串
    :return: <float/int> 提取的数字
    """
    if regex := re.search("[0-9,.]+(?=亿)", text):
        return int(float(regex.group().replace(",", "")) * 10000 * 10000)
    elif regex := re.search("[0-9,.]+(?=万)", text):
        return int(float(regex.group().replace(",", "")) * 10000)
    elif regex := re.search("[0-9,]+", text):
        return int(regex.group().replace(",", ""))
    elif regex := re.search("[0-9,.]+", text):
        return float(regex.group().replace(",", ""))
    else:
        return None


if __name__ == "__main__":
    print(number("38.5万粉丝"))
