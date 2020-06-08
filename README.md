# CxSpider
长行的爬虫合集，包括：微博热搜榜实时爬虫、

## 爬虫列表

### 1. Twitter用户信息爬虫(twitter.user_info)

> **@author** ChangXing
>
> **@version** 4.1
>
> **@create** 2017.12.25
>
> **@revise** 2020.06.08

使用第三方模块twitter-scraper采集Twitter用户信息；因为该模块采集的粉丝数和关注数可能存在偏差，因此再通过Selenium抓取Twitter用户信息，以更正该模块采集的数量。

* 采集信息：粉丝数和关注数为twitter-scraper采集并配合Selenium爬虫检查，其他字段为twitter-scraper采集。
* 应用配置：无需使用代理IP，需要使用Selenium

| 字段名          | 字段内容                                     |
| --------------- | -------------------------------------------- |
| name            | Twitter用户名                                |
| username        | Twitter用户唯一名称(@中的名字)               |
| birthday        | Twitter用户生日                              |
| biography       | Twitter用户介绍                              |
| website         | Twitter用户网站                              |
| profile_photo   | Twitter用户头像图的Url                       |
| likes_count     | Twitter用户的被点赞数                        |
| tweets_count    | Twitter用户的推文数                          |
| followers_count | Twitter用户的粉丝数(关注数:被多少人关注)     |
| following_count | Twitter用户的关注数(正在关注数:关注了多少人) |

### 2. Twitter用户推文爬虫(twitter.user_tweet)

> **@author** ChangXing
>
> **@version** 4.0
>
> **@create** 2017.12.30
>
> **@revise** 2020.06.08

采集指定Twitter用户在指定时间范围内的推文列表。

* 采集信息：使用Twitter搜索页面进行采集，单一用户的单次采集可追溯数量有限，不宜单次采集过长的时间跨度，可分为多次采集
* 应用配置：无需使用代理IP，需要使用Selenium

| 字段名   | 字段内容           |
| -------- | ------------------ |
| tweet_id | 推文ID             |
| time     | 推文发布时间       |
| text     | 推文内容文本       |
| replies  | 推文回复数         |
| retweets | 推文转推数         |
| likes    | 推文喜欢数(点赞数) |

### 3. 微博热搜榜实时爬虫(weibo.hot_ranking)

> **@author** ChangXing
>
> **@Version** 1.1
>
> **@create** 2020.05.29
>
> **@revise** 2020.06.08

定时采集微博热搜榜。

* 采集信息：每5分钟采集1次，每次约50条记录→每天约14400条记录
* 数据清洗：热搜榜置顶热搜（固定第1条）和广告热搜（标注推荐）
* 应用配置：无需使用代理IP、无需使用Selenium

| 字段名     | 字段内容   |
| ---------- | ---------- |
| fetch_time | 采集时间   |
| ranking    | 热搜排名   |
| keyword    | 热搜关键词 |
| heat       | 热搜热度   |
| icon       | 热搜标志   |

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

### Python/Pip环境

##### 必备环境

* **Python >= 3.8.0**
* requests >= 2.23.0
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

##### Selenium相关环境

* selenium >= 3.141.0
  * urllib3 >= 1.25.9

##### Twitter用户信息爬虫

* twitter-scraper >= 0.4.1
  * requests-html >= 0.10.0
  * MachanicalSoup >= 0.12.0

 











