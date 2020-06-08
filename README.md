# CxSpider
长行编写的爬虫的合集。包括如下爬虫：

| 网站              | 爬虫                         | 爬虫路径                 |
| ----------------- | ---------------------------- | ------------------------ |
| 微博              | 微博热搜榜实时爬虫           | weibo.hot_ranking        |
| Twitter           | Twitter用户信息爬虫          | twitter.user_info        |
| Twitter           | Twitter用户推文爬虫          | twitter.user_tweet       |
| WanPlus(玩加电竞) | 英雄联盟每日比赛列表爬虫     | wanplus.lol_date_list    |
| WanPlus(玩加电竞) | 英雄联盟比赛包含场次列表爬虫 | wanplus.lol_match_list   |
| WanPlus(玩加电竞) | 英雄联盟场次详细信息爬虫     | wanplus.lol_match_info   |
| 中国知网          | 中国知网期刊包含刊期列表爬虫 | cnki.issue_list          |
| 中国知网          | 英雄联盟比赛包含场次列表爬虫 | cnki.article_list        |
| 虎牙              | 虎牙直播弹幕爬虫             | huya.barrage_of_live     |
| 斗鱼              | 斗鱼直播弹幕爬虫             | douyu.barrage_of_live    |
| Bilibili(B站)     | Bilibili直播弹幕爬虫         | bilibili.barrage_of_live |

本合集中所有爬虫仅可用于学习、研究用途，不允许用于任何商业用途。如使将本合集中的任意爬虫用于商业用途，后果自负。

## 爬虫详情

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

### 3. 知网期刊包含刊期列表爬虫(cnki.issue_list)

> @author: ChangXing
> 
> @version: 1.1
> 
> @create: 2019.11.02
> 
> @revise: 2020.06.08

采集中国知网中指定期刊所有刊期的列表，刊期包括年份和在该年的序号。

* 采集参数：需要指定期刊的pcode、pykm共2个属性作为参数才可以采集
* 应用配置：无需使用代理IP，无需使用Selenium

### 4. 知网刊期包含论文列表爬虫(cnki.article_list)

> @author: ChangXing
>
> @version: 1.1
>
> @create: 2019.11.02
>
> @revise: 2020.06.08

采集中国知网中指定刊期所有论文的列表。

* 采集参数：需要指定刊期的pcode、pykm、年份、年序号共4个属性作为参数才可以采集
* 应用配置：无需使用代理IP，无需使用Selenium

| 字段名       | 字段内容                         |
| ------------ | -------------------------------- |
| title        | 论文标题                         |
| column       | 论文所在的栏目                   |
| db_code      | 论文Url的第1个参数               |
| file_name    | 论文Url的第2个参数               |
| db_name      | 论文Url的第3个参数               |
| team_a_score | LOL比赛的第1个参赛队伍的小场得分 |
| team_b_score | LOL比赛的第2个参赛队伍的小场得分 |
| contest_name | 比赛的全名                       |

### 5. 虎牙直播弹幕爬虫(huya.barrage_of_live)

> @author: ChangXing
>
> @version: 1.2
>
> @create: 2019.11.24
>
> @revise: 2020.06.08

使用Selenium模拟浏览器，采集虎牙直播间中的弹幕。

* 应用配置：无需使用代理IP，需要使用Selenium

| 字段名     | 字段内容                                               |
| ---------- | ------------------------------------------------------ |
| bid        | 弹幕ID                                                 |
| type       | 弹幕类型                                               |
| fetch_time | 弹幕采集时间（因实时采集，因此也可以视为弹幕发布时间） |
| user_name  | 弹幕发布者名称                                         |
| user_noble | 弹幕发布者贵族等级                                     |
| content    | 弹幕内容                                               |
| gift_name  | 赠送礼物弹幕的礼物名称                                 |
| gift_num   | 赠送礼物弹幕的礼物数量                                 |
| other      | 弹幕的其他信息                                         |

### 6. 斗鱼直播弹幕爬虫(douyu.barrage_of_live)

> @author: ChangXing
>
> @version: 1.2
>
> @create: 2019.11.24
>
> @revise: 2020.06.08

使用Selenium模拟浏览器，采集斗鱼直播间中的弹幕。

* 应用配置：无需使用代理IP，需要使用Selenium

| 字段名     | 字段内容                                               |
| ---------- | ------------------------------------------------------ |
| bid        | 弹幕ID                                                 |
| type       | 弹幕类型                                               |
| fetch_time | 弹幕采集时间（因实时采集，因此也可以视为弹幕发布时间） |
| user_name  | 弹幕发布者名称                                         |
| user_level | 弹幕发布者等级                                         |
| content    | 弹幕内容                                               |
| text       | 弹幕其他信息                                           |

### 7. Bilibili直播弹幕爬虫(bilibili.barrage_of_live)

> @author: ChangXing
>
> @version: 1.2
>
> @create: 2019.11.24
>
> @revise: 2020.06.08

使用Selenium模拟浏览器，采集Bilibili直播间中的弹幕。

* 应用配置：无需使用代理IP，需要使用Selenium

| 字段名     | 字段内容                                               |
| ---------- | ------------------------------------------------------ |
| bid        | 弹幕ID                                                 |
| type       | 弹幕类型                                               |
| fetch_time | 弹幕采集时间（因实时采集，因此也可以视为弹幕发布时间） |
| user_name  | 弹幕发布者名称                                         |
| user_id    | 弹幕发布者ID                                           |
| content    | 弹幕内容                                               |

### 8. WanPlus英雄联盟每日比赛列表爬虫(wanplus.lol_date_list)

> **@author** ChangXing
>
> **@version** 1.1
>
> **@create** 2020.04.20
>
> **@revise** 2020.06.08

采集WanPlus中每天英雄联盟的比赛列表。

* 目标Url：https://www.wanplus.com/lol/schedule
* 实际请求的Ajax：https://www.wanplus.com/ajax/schedule/list
* 应用配置：无需使用代理IP、无需使用Selenium

| 字段名           | 字段内容                             |
| ---------------- | ------------------------------------ |
| race_id          | WanPlus中LOL比赛的ID                 |
| team_a_name      | LOL比赛的第1个参赛队伍的名字         |
| team_b_name      | LOL比赛的第2个参赛队伍的名字         |
| start_time       | LOL比赛的开始时间                    |
| team_a_score     | LOL比赛的第1个参赛队伍的小场得分     |
| team_b_score     | LOL比赛的第2个参赛队伍的小场得分     |
| contest_name     | 比赛的全名                           |
| match_name       | 比赛的简称                           |
| team_a_score_per | LOL比赛的第1个参赛队伍各个小场的得分 |
| team_b_score_per | LOL比赛的第2个参赛队伍各个小场的得分 |

### 9. WanPlus英雄联盟比赛包含场次列表爬虫(wanplus.lol_match_list)

> **@author** ChangXing
>
> **@version** 1.1
>
> **@create** 2020.04.20
>
> **@revise** 2020.06.08

采集WanPlus中每场英雄联盟比赛包含的具体场次(一局游戏)列表。

* 目标Url：https://www.wanplus.com/schedule/58822.html
* 应用配置：无需使用代理IP、无需使用Selenium

### 10. WanPlus英雄联盟场次详细信息爬虫(wanplus.lol_match_info)

> **@author** ChangXing
>
> **@version** 1.1
>
> **@create** 2020.04.20
>
> **@revise** 2020.06.08

采集WanPlus中每场英雄联盟场次(一局游戏)包含的具体详细信息。

* 目标Url(实际请求的Ajax)：https://www.wanplus.com/ajax/matchdetail/65029?_gtk=345357323
* 应用配置：无需使用代理IP、无需使用Selenium

### 11. 微博热搜榜实时爬虫(weibo.hot_ranking)

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

 











