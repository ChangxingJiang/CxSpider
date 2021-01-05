import re
from typing import List, Dict

import crawlertool as tool


class SpiderAcfunVideo(tool.abc.SingleSpider):
    """AcFun视频信息爬虫"""

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

    def running(self, page_url) -> List[Dict]:
        # 获取视频基本信息
        response = tool.do_request(page_url, headers=self._HEADERS).text
        title = re.search(r"(?<=<title>)[^<]+(?=</title>)", response).group()  # 提取视频标题
        video_id = re.search(r"(?<=\"vid\":\")\d+(?=\",)", response).group()  # 提取视频ID
        resource_id = re.search(r"(?<=\"ac\":\")\d+(?=\",)", response).group()  # 提取视频资源ID

        # 获取视频下载Url
        rep_info = tool.do_request(self._DOWNLOAD_URL.format(video_id, resource_id), headers=self._HEADERS)
        video_url = rep_info.json()["playInfo"]["streams"][0]["playUrls"][0]

        # 返回结果
        return [{
            "Title": title,
            "Download Url": video_url
        }]


# ------------------- 单元测试 -------------------
if __name__ == "__main__":
    print(SpiderAcfunVideo().running(page_url="https://www.acfun.cn/v/ac16986343"))
