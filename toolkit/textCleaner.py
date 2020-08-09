import re
from typing import List

from pyhanlp import HanLP


class TextCleaner:
    """
    文本清洗工具类

    基本清洗:

        clear_empty() 清除空白字符，包括空格、制表符、换页符

    英文文本清洗：

        upper() 将英文字母转换为大写
        lower() 将英文字母转换为小写

    中文文本清洗：

        simplify() 将繁体字转换为简体字
        halve_width() 将所有字符转化为半角字符
        full_width() 将所有字符转化为全角字符

    小说文本清洗：

        novel_unify_ellipsis() 统一省略号形式：。。。->...
        novel_clear_indentation() 移除行首缩进空格
        novel_clear_enter_in_quotation() 清理引号中的多行硬回车
        novel_clear_enter_in_quotation() 清理引号中的多行硬回车
        novel_clear_enter_in_paragraph() 清理文段内的硬回车
        novel_clear_invalid_line_by_mark(marks) 依据特殊文本清除无效行
        novel_clear_invalid_line_by_pattern(patterns) 依据正则表达式(多行模式)清除无效行
        novel_clear_line_in_brackets() 清除完全存在于括号中的行
        novel_clear_empty_line() 清除空行

    返回结果：

        fetch_number() 提取字符串中的数字并返回数值格式
        result() 返回字符串格式结果
        __str__() 返回字符串格式结果

    """

    def __init__(self, data: str):
        self._data = data

    def clear_empty(self):
        self._data = re.sub(r"\s", "", self._data)
        return self

    def upper(self):
        """将英文字母转换为大写"""
        self._data.upper()
        return self

    def lower(self):
        """将英文字母转换为小写"""
        self._data.lower()
        return self

    def simplify(self):
        """将繁体字转换为简体字"""
        self._data = HanLP.convertToSimplifiedChinese(self._data)
        return self

    def halve_width(self):
        """将所有字符转化为半角字符"""
        ans = []
        for uchar in self._data:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 转换空格
                inside_code = 32
            elif 65281 <= inside_code <= 65374:  # 转换空格以外的全角字符
                inside_code -= 65248
            ans.append(chr(inside_code))
        self._data = "".join(ans)
        return self

    def full_width(self):
        """将所有字符转化为全角字符"""
        ans = []
        for uchar in self._data:
            inside_code = ord(uchar)
            if inside_code == 32:  # 半角空格直接转化
                inside_code = 12288
            elif 32 <= inside_code <= 126:  # 半角字符（除空格）根据关系转化
                inside_code += 65248
            ans.append(chr(inside_code))
        self._data = "".join(ans)
        return self

    def novel_unify_ellipsis(self):
        """[小说]统一省略号形式：。。。->..."""
        self._data = self._data.replace("。。。", "...")
        return self

    def novel_clear_indentation(self):
        """[小说]移除行首缩进空格"""
        # self._data = re.sub("(?<=\n)[ 　]+", "", self._data)  # 单行模式
        self._data = re.sub("^[ 　]+", "", self._data, flags=re.M)  # 多行模式
        return self

    def novel_clear_enter_in_quotation(self):
        """
        [小说]清理引号引住内容中的硬回车

        例1：
            是不胜之喜。韦春芳见七个媳妇个个如花似玉,心想:“小宝这小贼
            挑女人的眼力倒不错,他来开院子,一定发大财。”

        例2：
            道:“我怎么知道?”韦小宝皱眉道:“你肚子里有我之前,接过什么客
            人?”韦春芳道:“那时你娘我标致得很,每天有好几个客人,我怎么
            记得这许多?”
        """

        def delete(matched):
            return matched.group(0).replace("\n", "")

        self._data = re.sub("“[^”]*\n[^”]*”", delete, self._data)
        return self

    def novel_clear_enter_in_paragraph(self):
        """
        [小说]清理文段内的硬回车

        清理依据：硬回车之前后两行均包含通常出现于文段中的标点符号(,。!?)

        例1：
            这一下吓得魂不附体,心想怎么真的将他杀死了,扑将过去,叫道:
            “相公,相公!”只见韦小宝身子僵直,心中更慌,忙伸手去扶。韦

        例2：
            西奔出十余丈,倏地跃下马来,冲向西北,左穿右插,不知如何,竟
            又回了人圈,笑吟吟的站在当地,谁也没看清他是怎么进来的。
        """

        def delete(matched):
            return matched.group(0).replace("\n", "")

        self._data = re.sub("[,，?？!！:：;；。、“”‘’][\u4e00-\u9fa5]+\n[\u4e00-\u9fa5]*[,，?？!！:：;；。、“”‘’]", delete, self._data)
        return self

    def novel_clear_invalid_line_by_mark(self, marks: List[str]):
        """
        [小说]依据特殊文本清除无效行

        例1：
            输入:Vikings <jobjob@gdup3.gd.cei.go.cn>  mark = "输入:"

        例2：
            Typed by Wang Jian(王健)and Bai Li(白力)  mark = "Typed by"

        :param marks: <List[str]> 无效行包含的特殊文本
        """
        for mark in marks:
            self._data = re.sub("^.*" + mark + ".*$", "", self._data, flags=re.M)  # 多行模式
        return self

    def novel_clear_invalid_line_by_pattern(self, patterns: List[str]):
        """
        [小说]依据正则表达式(多行模式)清除无效行

        例1：
            Vikings <jobjob@gdup3.gd.cei.go.cn>

        :param patterns: <List[str]> 无效行的正则表达式
        """
        for pattern in patterns:
            self._data = re.sub(pattern, "", self._data, flags=re.M)  # 多行模式
        return self

    def novel_clear_line_in_brackets(self):
        """
        [小说]清除完全存在于括号中的行

        例1：
            <图片>

        例2：
            (全书完)
        """
        self._data = re.sub(r"^[(<\[{][^)>\]}]*[)>\]}]$", "", self._data, flags=re.M)  # 多行模式
        return self

    def novel_clear_empty_line(self):
        """[小说]清除空行"""
        self._data = re.sub("(\r?\n)+", "\n", self._data)
        self._data = re.sub("\n$", "", self._data)  # 处理整个文本最后的空行
        return self

    def fetch_number(self):
        """
        提取字符串中的数字

        可以提取的数字格式(优先级从高到低)：
        [0-9,.]+(?=亿)
        [0-9,.]+(?=万)
        [0-9,]+
        [0-9,.]+

        :return: <float/int> 提取的数字
        """
        if regex := re.search("[0-9,.]+(?=亿)", self._data):
            return int(float(regex.group().replace(",", "")) * 10000 * 10000)
        elif regex := re.search("[0-9,.]+(?=万)", self._data):
            return int(float(regex.group().replace(",", "")) * 10000)
        elif regex := re.search("[0-9,]+", self._data):
            return int(regex.group().replace(",", ""))
        elif regex := re.search("[0-9,.]+", self._data):
            return float(regex.group().replace(",", ""))
        else:
            return None

    def result(self):
        """获取文本清洗结果"""
        return self._data

    def __str__(self):
        return self._data
