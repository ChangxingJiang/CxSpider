# coding=utf-8

"""
MySQL相关工具类
"""

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

    def create(self, sql: str):
        """
        [CREATE]创建数据表到MySQL数据库

        :param sql: <str> 创建数据表的SQL语句
        """
        try:
            mysql_cursor = self.connect.cursor()
            mysql_cursor.execute(sql)
            return True
        except mysql.connector.errors.ProgrammingError:
            return False

    def select(self, table_name: str, column_list: list, sql_where: str = ""):
        """ SELECT读取MySQL数据库的数据
        :param table_name: <str> 需要读取的MySQL数据表名称
        :param column_list: <list:str> 需要读取的字段名称列表
        :param sql_where: <str> 在执行SELECT语句时是否添加WHERE子句(默认为空,如添加应以WHERE开头)
        :return: <list> 读取的数据结果
        """
        mysql_cursor = self.connect.cursor()
        mysql_cursor.execute(sql_select(table_name, column_list, sql_where))  # 生成并执行SELECT语句
        mysql_results = mysql_cursor.fetchall()  # 获取SQL语句执行的返回多行记录的结果
        select_result = []
        for mysql_result in mysql_results:  # 遍历:SQL语句检索的各行记录
            if len(column_list) > 1:  # 处理读取字段数超过1个的情况
                select_item = []
                for i in range(len(column_list)):
                    select_item.append(mysql_result[i])
                select_result.append(select_item)
            elif len(column_list) == 1:  # 处理读取字段数为1个的情况
                select_result.append(mysql_result[0])
        return select_result

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


def sql_insert_pure(table_name: str, data_list: list):
    """
    [生成SQL语句]INSERT语句(纯粹SQL语句,部分sql和val)

    :param table_name: <str> 需要写入的MySQL数据表名称
    :param data_list: <list:list> 需要写入的多条记录(所有记录的字段名与第一条记录的字段名统一)
    :return: <str> SQL语句部分
    """
    if len(data_list) == 0:
        return None

    # 生成SQL语句
    column_list = []
    column_part = ""  # SQL语句列名部分
    for column in data_list[0]:
        column_list.append([column, type(data_list[0][column])])
        column_part += "`" + column + "`,"
    column_part = re.sub(",$", "", column_part)

    # 生成写入数据
    value_list = []
    for data in data_list:
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

    return "INSERT INTO " + table_name + " (" + column_part + ") VALUES " + ",".join(value_list)  # 拼接SQL语句


def sql_select(table_name: str, column_list: list, sql_where: str = ""):
    """
    [生成SQL语句]SELECT语句

    :param table_name: <str> 需要SELECT的表单名称
    :param column_list: <list:str> 需要读取的字段名称列表
    :param sql_where: <str> 在SELECT时执行的WHERE子句(默认为空,如添加应以WHERE开头)
    :return: <str> 生成完成的SELECT(MySQL)语句
    """
    sql = "SELECT "
    for column in column_list:
        sql += column + ","
    return re.sub(",$", " FROM " + table_name + " " + sql_where, sql)


if __name__ == "__main__":
    pass
