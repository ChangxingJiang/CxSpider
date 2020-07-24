"""
AcFun视频信息爬虫

@author: ChangXing
@version: 1.0
@create: 2020.07.24
@revise: -
"""

import re

import requests


def crawler(url: str):
    headers = {
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25"
    }
    info_url = "https://api-new.acfunchina.com/rest/app/play/playInfo/mp4?videoId={}&resourceId={}&resourceType=2&mkey=AAHewK3eIAAyMjAzNTI2NDMAAhAAMEP1uwS3Vi7NYAAAAJumF4MyTTFh5HGoyjW6ZpdjKymALUy9jZbsMTBVx-F10EhxyvpMtGQbBCYipvkMShM3iMNwbMd9DM6r2rnOYRVEdr6MaJS4yxxlA_Sl3JNWup57qBCQzOSC7SZnbEsHTQ%3D%3D&market=xiaomi&product=ACFUN_APP&sys_version=10&app_version=6.20.0.915&boardPlatform=sdm845&sys_name=android&socName=UNKNOWN&appMode=0"

    # 获取视频基本信息
    response = requests.get(url, headers=headers)
    title = re.search(r"(?<=<title>)[^<]+(?=</title>)", response.text).group()  # 视频标题
    video_id = re.search(r"(?<=\"vid\":\")\d+(?=\",)", response.text).group()  # 视频ID
    resource_id = re.search(r"(?<=\"ac\":\")\d+(?=\",)", response.text).group()  # 视频资源ID

    # 获取视频Url
    rep_info = requests.get(info_url.format(video_id, resource_id), headers=headers)
    video_url = rep_info.json()["playInfo"]["streams"][0]["playUrls"][0]
    return {"title": title, "videos": video_url}


if __name__ == "__main__":
    print(crawler("https://www.acfun.cn/v/ac16986343"))
