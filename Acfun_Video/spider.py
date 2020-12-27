"""
AcFun视频信息爬虫（包括下载地址）

需要第三方模块：
Utils4R >= 0.0.6

@Author: 长行
@Update: 2020.10.18
"""

import re

import crawlertool as tool
import requests


class Spider(tool.abc.SingleSpider):
    # 执行请求的请求头
    _HEADERS = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
    }

    # 视频信息的Url
    _DOWNLOAD_URL = ("https://api-new.acfunchina.com/rest/app/play/playInfo/mp4"
                     "?videoId={}"
                     "&resourceId={}"
                     "&resourceType=2"
                     "&mkey=AAHewK3eIAAyMjAzNTI2NDMAAhAAMEP1uwS3Vi7NYAAAAJumF4MyTTFh5HGoyjW6ZpdjKymALUy9jZbsMTBVx-F10EhxyvpMtGQbBCYipvkMShM3iMNwbMd9DM6r2rnOYRVEdr6MaJS4yxxlA_Sl3JNWup57qBCQzOSC7SZnbEsHTQ%3D%3D"
                     "&market=xiaomi"
                     "&product=ACFUN_APP"
                     "&sys_version=10"
                     "&app_version=6.20.0.915"
                     "&boardPlatform=sdm845"
                     "&sys_name=android"
                     "&socName=UNKNOWN"
                     "&appMode=0")

    def running(self, page_url: str):
        # 获取视频基本信息
        response = requests.get(page_url, headers=self._HEADERS).text
        title = re.search(r"(?<=<title>)[^<]+(?=</title>)", response).group()  # 提取视频标题
        video_id = re.search(r"(?<=\"vid\":\")\d+(?=\",)", response).group()  # 提取视频ID
        resource_id = re.search(r"(?<=\"ac\":\")\d+(?=\",)", response).group()  # 提取视频资源ID

        # 获取视频下载Url
        rep_info = requests.get(self._DOWNLOAD_URL.format(video_id, resource_id), headers=self._HEADERS)
        video_url = rep_info.json()["playInfo"]["streams"][0]["playUrls"][0]

        # 返回结果
        return {
            "视频标题": title,
            "视频下载地址": video_url
        }


if __name__ == "__main__":
    spider = Spider()
    print(spider.running(page_url="https://www.acfun.cn/v/ac16986343"))
