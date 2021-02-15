import datetime
import json
import time
from typing import List, Dict

import crawlertool as tool


class SpiderWanplusLolDateList(tool.abc.SingleSpider):
    """WanPlus英雄联盟每日比赛列表爬虫"""

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
    _DATE_LIST_DATA = {
        "_gtk": "345357323",
        "game": "2",
        "time": "1571500800",
        "eids": "",
    }  # 列表请求的表单数据

    def running(self, start_date, end_date) -> List[Dict]:
        result = []

        # 统计需要抓取的日期列表
        all_date_list = list()  # 需要获取的日期列表
        curr_date = end_date
        while curr_date >= start_date:
            all_date_list.append(curr_date.strftime("%Y%m%d"))
            curr_date += datetime.timedelta(days=-1)
        # print("需要抓取的日期总数:", len(all_date_list), all_date_list)

        if len(all_date_list) == 0:  # 若没有需要抓取的日期则结束运行
            return result

        # 统计需要追溯的日期所在的周的时间戳
        need_date_list = list()  # 需要抓取的时间戳列表(所有的周日+最早的一天)
        for curr_date_str in all_date_list:
            curr_date = datetime.datetime.strptime(curr_date_str, "%Y%m%d")
            if curr_date.weekday() == 0:  # 若时间戳为周日
                need_date_list.append(curr_date_str)
        need_date_list.append(all_date_list[-1])  # 添加最早的一天
        # print("需要抓取的时间戳总数:", len(need_date_list))

        # 格式化日期，方便比较
        end_date = end_date.strftime("%Y%m%d")
        start_date = start_date.strftime("%Y%m%d")

        # 依据时间戳抓取比赛数据
        for i in range(len(need_date_list)):
            curr_date_str = need_date_list[i]
            # print("正在抓取时间戳:", i + 1, "/", len(need_date_list), "(", curr_date_str, ")")
            curr_date_timestamp = str((datetime.datetime.strptime(curr_date_str, "%Y%m%d") - datetime.datetime(1970, 1, 1)).total_seconds())
            self._DATE_LIST_DATA["time"] = curr_date_timestamp  # 列表请求的表单数据
            response = tool.do_request(self._DATE_LIST_URL, method="post", headers=self._DATE_LIST_HEADERS, data=self._DATE_LIST_DATA)
            # print(response.content)
            if response.status_code == 200:
                response_json = json.loads(response.content.decode())
                # print(response_json)
                for curr_date_str, date_info in response_json["data"]["scheduleList"].items():
                    if int(end_date) >= int(curr_date_str) >= int(start_date):
                        if date_info["list"]:
                            for match in date_info["list"]:
                                result.append({
                                    "date": curr_date_str,
                                    "race_id": match["scheduleid"],
                                    "team_a_name": match["oneseedname"],
                                    "team_b_name": match["twoseedname"],
                                    "start_time": match["starttime"],
                                    "team_a_score": match["onewin"],
                                    "team_b_score": match["twowin"],
                                    "contest_name": match["ename"],
                                    "match_name": match["groupname"],
                                    "team_a_score_per": match["oneScore"],
                                    "team_b_score_per": match["twoScore"],
                                })
            time.sleep(5)

        return result


# ------------------- 单元测试 -------------------
if __name__ == "__main__":
    print(SpiderWanplusLolDateList().running(
        start_date=datetime.datetime.today() + datetime.timedelta(days=-7),  # 抓取开始日期
        end_date=(datetime.datetime.today() + datetime.timedelta(days=7))  # 抓取结束日期
    ))
