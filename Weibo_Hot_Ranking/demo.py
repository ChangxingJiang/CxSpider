import crawlertool as tool

from spider import SpiderWeiboHotRanking


class Spider(SpiderWeiboHotRanking):
    """重写SpiderWeiboHotRanking类"""

    def __init__(self, interval, mysql):
        super().__init__(interval)
        self.mysql = mysql

    def write(self, data):
        # 将结果写入到数据库
        self.mysql.insert(table="weibo", data=data)


if __name__ == "__main__":
    spider = Spider(interval=5, mysql=tool.db.DefaultMySQL())
    spider.start()
