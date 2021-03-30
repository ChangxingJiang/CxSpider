import json
import time
from datetime import datetime
from datetime import timedelta
from typing import List, Dict

import crawlertool as tool


class SpiderWanplusLolDateList(tool.abc.SingleSpider):
    """WanPlus英雄联盟每日比赛列表爬虫（最多追溯365天）"""

    _COLUMNS = ["schedule_id", "date", "time", "event_id", "event_name", "event_group_name", "stage_id", "bo_num",
                "team_a_id", "team_a_name", "team_b_id", "team_b_name",
                "team_a_win", "team_b_win", "team_a_score", "team_b_score"]

    # 列表请求的url
    _DATE_LIST_URL = "https://www.wanplus.com/ajax/schedule/list"

    # 列表请求的headers
    _DATE_LIST_HEADERS = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "no-cache",
        "content-length": "43",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://www.wanplus.com",
        "pragma": "no-cache",
        "referer": "https://www.wanplus.com/lol/schedule",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        "x-csrf-token": "345357323",
        "x-requested-with": "XMLHttpRequest"
    }

    # 列表请求的表单数据
    _DATE_LIST_DATA = {
        "_gtk": "345357323",
        "game": "2",
        "time": "1571500800",
        "eids": "",
    }

    def running(self, start_date, end_date) -> List[Dict]:
        # 初始化返回结果数据
        result = []

        # ----- 计算所有需要抓取的日期列表 -----
        all_date_list = []  # 需要获取的日期列表
        curr_date = end_date
        while curr_date >= start_date:
            all_date_list.append(curr_date.strftime("%Y%m%d"))
            curr_date += timedelta(days=-1)

        # 若没有需要抓取的日期则完成采集
        if len(all_date_list) == 0:
            return result

        # ----- 计算实际需要请求的日期列表 -----
        # 每一次请求均会返回该日所在周7天的数据，因此只需要请求每周的周日即可，和最后一个还没有到周日的周即可
        need_date_list = []
        # 如果最后一周还没有到周日，则添加最后一周的最后一天
        if datetime.strptime(all_date_list[0], "%Y%m%d").weekday() != 0:
            need_date_list.append(all_date_list[0])
        # 添加之前每一周的周日
        for curr_date in all_date_list:
            if datetime.strptime(curr_date, "%Y%m%d").weekday() == 0:
                need_date_list.append(curr_date)

        # ----- 依据时间戳抓取比赛数据 -----
        for i in range(len(need_date_list)):

            print("当前抓取:", self.format_date(need_date_list[i]), "(", i + 1, "/", len(need_date_list), ")")
            curr_date = need_date_list[i]

            # 计算请求参数并执行请求
            curr_date_timestamp = str((datetime.strptime(curr_date, "%Y%m%d") - datetime(1970, 1, 1)).total_seconds())
            self._DATE_LIST_DATA["time"] = curr_date_timestamp
            response = tool.do_request(
                self._DATE_LIST_URL, method="post",
                headers=self._DATE_LIST_HEADERS, data=self._DATE_LIST_DATA
            )

            if response.status_code != 200:
                print("请求失败!")
                continue

            # 解析请求的返回结果
            response_json = json.loads(response.content.decode())
            for curr_date, date_info in response_json["data"]["scheduleList"].items():  # 遍历该周的每一天
                print("当前抓取日期:", self.format_date(curr_date))
                if int(start_date.strftime("%Y%m%d")) <= int(curr_date) <= int(end_date.strftime("%Y%m%d")):
                    if date_info["list"]:  # 检查当日是否有比赛
                        for match in date_info["list"]:  # 遍历该日的每一场比赛
                            result.append({
                                "schedule_id": int(match["scheduleid"]),  # 比赛ID(一场完整的BO1/BO3/BO5的比赛称为比赛)
                                "date": self.format_date(curr_date),  # 比赛日期
                                "time": match["starttime"],  # 比赛时间:比赛开始时间
                                "event_id": int(match["eid"]),  # 赛事ID
                                "event_name": match["ename"],  # 赛事名称
                                "event_group_name": match["groupname"],  # 赛事赛段
                                "stage_id": int(match["stageid"]),  # 疑似赛事ID
                                "bo_num": int(match["bonum"]),  # 比赛场次:BO1=1,BO3=3,BO5=5
                                "team_a_id": int(match["oneseedid"]),  # 队伍A的ID
                                "team_a_name": match["oneseedname"],  # 队伍A的名称
                                "team_b_id": int(match["twoseedid"]),  # 队伍B的ID
                                "team_b_name": match["twoseedname"],  # 队伍B的名称
                                "team_a_win": int(match["onewin"]),  # 队伍A的获胜小场数
                                "team_b_win": int(match["twowin"]),  # 队伍B的获胜小场数
                                "team_a_score": str(match["oneScore"]),  # 队伍A的每小场得分
                                "team_b_score": str(match["twoScore"]),  # 队伍B的每小场得分
                            })

            # 执行延迟
            time.sleep(5)

        return result

    @staticmethod
    def format_date(string):
        return string[0:4] + "-" + string[4:6] + "-" + string[6:8]


# ------------------- 单元测试 -------------------
if __name__ == "__main__":
    print(SpiderWanplusLolDateList().running(
        start_date=datetime.today() + timedelta(days=-2),  # 抓取开始日期
        end_date=datetime.today() + timedelta(days=-1)  # 抓取结束日期
    ))
