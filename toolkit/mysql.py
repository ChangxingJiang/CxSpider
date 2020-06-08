import re

import mysql.connector

import environment as env


class MySQL:
    def __init__(self, host: str, database: str, user: str, password: str, use_unicode: bool = True):
        """
        MySQL连接对象构造器

        :param host: <str> 主机名
        :param database: <str> 数据库名
        :param user: <str> 用户名
        :param password: <str> 密码
        :param use_unicode: <bool> MySQL连接的use_unicode选项(默认=True)
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password

        # 构造MySQL链接
        self.connect = mysql.connector.connect(
            host=host, user=user, password=password, database=database, use_unicode=use_unicode
        )

    def insert(self, table_name: str, data: list):
        """
        [INSERT INTO]写入数据到MySQL数据库

        :param table_name: <str> 表名
        :param data: <list:dict> 需要写入的多条记录(所有记录的字段名与第一条记录的字段名统一)
        :return: <bool> 写入数据是否成功
        """
        # 处理需要写入的记录数为0的情况
        if len(data) == 0:
            return True

        # 处理需要写入的记录数不为0的情况
        try:
            mysql_cursor = self.connect.cursor()
            sql = sql_insert_pure(table_name, data)  # 生成SQL语句
            mysql_cursor.execute(sql)  # 执行SQL语句
            self.connect.commit()  # 数据表内容更新提交语句
            return mysql_cursor.rowcount
        except mysql.connector.errors.ProgrammingError:
            return False

    def __str__(self):
        return str({
            "Host": self.host,
            "Database": self.database,
            "User": self.user,
            "Password": self.password
        })


def connect(name):
    """
    连接环境配置中名为name的数据库

    :param name: <str> 存在于环境配置中的数据库名称
    :return: <toolkit.mysql.MySQL> MySQL连接对象
    """
    return MySQL(host=env.MYSQL_INFO[name]["Host"],
                 user=env.MYSQL_INFO[name]["User"],
                 password=env.MYSQL_INFO[name]["Password"],
                 database=env.MYSQL_INFO[name]["Database"])


def sql_insert_pure(table: str, datas: list):
    """ [生成SQL语句]INSERT语句(纯粹SQL语句,部分sql和val)
    :param table: <str> 需要写入的MySQL数据表名称
    :param datas: <list:list> 需要写入的多条记录(所有记录的字段名与第一条记录的字段名统一)
    :return: <str> SQL语句部分
    """
    if len(datas) == 0:
        return None

    # 生成SQL语句
    column_list = []
    column_part = ""  # SQL语句列名部分
    for column in datas[0]:
        column_list.append([column, type(datas[0][column])])
        column_part += "`" + column + "`,"
    column_part = re.sub(",$", "", column_part)

    # 生成写入数据
    value_list = []
    for data in datas:
        val_item = "("
        for column in column_list:
            if column[0] in data and data[column[0]] is not None:
                if column[1] == int or column[1] == float or column[1] == bool:
                    val_item += str(data[column[0]]) + ","
                else:
                    val_item += "'" + str(data[column[0]]).replace("'", "") + "',"
            else:
                if column[1] == int or column[1] == float:
                    val_item += "0,"
                else:
                    val_item += "'',"
        val_item = re.sub(",$", ")", val_item)
        value_list.append(val_item)

    return "INSERT INTO " + table + " (" + column_part + ") VALUES " + ",".join(value_list)  # 拼接SQL语句
