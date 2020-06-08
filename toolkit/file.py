import json
import os
from json import JSONDecodeError


def load_as_json(path, encoding="UTF-8"):
    """读取文件内容为Json格式

    :param path: <str> 文件路径
    :param encoding: <str> 编码格式
    """
    if os.path.exists(path):
        try:
            with open(path, encoding=encoding) as fr:
                return json.loads(fr.read())
        except FileNotFoundError:
            print("未找到文件:", path)
            return None
        except JSONDecodeError:
            print("目标文件不是Json文件:" + path)
            return None


def write_string(path, data, encoding="UTF-8", type="w"):
    """将字符串写入到文件中

    :param path: <str> 文件路径
    :param data: <str> 需要写入的字符串
    :param encoding: <str> 编码格式
    """
    try:
        with open(path, type, encoding=encoding) as fr:
            fr.write(data)
    except FileExistsError:
        print("文件存在,写入失败:", path, "(type=", type, ")")


def write_json(path, data, ensure_ascii=False):
    """将Json格式数据写入到文件中

    :param path: <str> 文件路径
    :param data: 需要写入的Json格式数据
    :param ensure_ascii: <bool> 是否不允许包含非ASCII编码字符
    """
    write_string(path, json.dumps(data, ensure_ascii=ensure_ascii))
