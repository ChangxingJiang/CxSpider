# CxSpider
ChangXing爬虫包

## 爬虫列表

### 1. 微博热搜榜实时爬虫

> **@author** ChangXing
>
> **@Version** 1.1
>
> **@create** 2020.05.29
>
> **@revise** 2020.06.08

##### 数据说明

数据表：weibo_hot_ranking

数据结构：fetch_time=采集时间、ranking=热搜排名、keyword=热搜关键词、heat=热搜热度、icon=热搜标志

##### 采集说明

* 采集信息：每5分钟采集1次，每次约50条记录→每天约14400条记录
* 数据清洗：热搜榜置顶热搜（固定第1条）和广告热搜（标注推荐）
* 无需使用代理IP、无需使用Selenium



## 环境变量

爬虫功能的正常使用需要配置如下环境变量，可以直接修改environment.py中的环境变量值，也可以修改配置Json文件。

| 变量名               | 必选 | 功能 | 变量含义                       |
| -------------------- | ---- | ---- | ------------------------------ |
| PROXY_BELONG         | 否   | 代理IP |代理IP:所属公司                |
| PROXY_API            | 是   | 代理IP |代理IP:API的Url                |
| CHROMEDRIVER_PATH    | 是   | Selenium |ChromeDriver可执行文件路径     |
| CHORME_LOCATION      | 是   | Selenium |Chrome浏览器可执行文件路径     |
| CHROME_USERDATA_PATH | 是   | Selenium |Chrome浏览器用户数据文件夹路径 |
| CHROME_DOWNLOAD_PATH | 是   | Selenium |Chrome浏览器下载文件存储路径   |
| MYSQL_INFO           | 是   | MySQL |读取MySQL相关设置              |

## 环境配置

* **Python >= 3.8.0**
* Requests >= 2.23.0
  * idna >= 2.9
  * urllib3 >= 1.25.9
  * certifi >= 2020.4.5.1
  * chardet >= 3.0.4
* bs4 >= 0.0.1
  * beautifulsoup4 >= 4.9.0
  * soupsieve >= 2.0
* apscheduler >= 3.6.3
  * pytz >= 2019.3
  * six >= 1.14.0
  * tzlocal >= 2.1
  * setuptools
* mysql-connector >= 2.2.9
* lxml >= 4.5.0



 











