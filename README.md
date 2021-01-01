# CxSpider 长行的爬虫合集
本项目为爬虫合集，包括两部分，其一为本合集自行实现的爬虫，其二为本合集收录的其他爬虫。

对于本合集自行设计的爬虫，本合集统一了爬虫的配置方式、调用方式和返回结果格式，并遵循如下原则：

1. 每个Python脚本（.py文件）仅依赖于发布在pypi（可以通过pip安装）的工具即自身，方便直接复制代码来使用爬虫。
2. 爬虫返回结果统一为字典列表格式，并在工具类中配有将这种格式写入csv、Excel和MySQL的工具函数。
3. 将所有爬虫发布到pypi的cxspider模块（`pip install cxspider`），方便直接调用。

对于本合集收录的爬虫，均为发布在Github或博客中的爬虫，本项目作者测试基本无误后收录。本合集将其中的部分爬虫改变为本合集的统一格式，以方便调用，但会明确标注爬虫的来源。

## 爬虫列表

| ID     | 网站               | 爬虫                               | 爬虫路径                     | 状态   |
| ------ | ------------------ | ---------------------------------- | ---------------------------- | ------ |
| S-01-1 | 微博               | 微博热搜榜实时爬虫                 | weibo.hot_ranking            | 正常   |
| S-02-1 | Twitter            | Twitter用户推文爬虫                | twitter.user_tweet           | 待更新 |
| S-02-2 | Twitter            | Twitter用户信息爬虫                | twitter.user_info            | 正常   |
| S-03-1 | Facebook           | Facebook用户推文爬虫               | facebook.user_tweet          | 正常   |
| V-01-1 | Bilibili           | B站UP主发布视频列表爬虫【Demo】    | bilibili.user_video_list     | 正常   |
| V-02-1 | AcFun              | AcFun视频信息爬虫（包括下载地址）  | acfun.video                  | 正常   |
| G-01-1 | WanPlus-玩加电竞   | 英雄联盟每日比赛列表爬虫           | wanplus.lol_date_list        | 正常   |
| G-01-2 | WanPlus-玩加电竞   | 英雄联盟比赛包含场次列表爬虫       | wanplus.lol_match_list       | 正常   |
| G-01-3 | WanPlus-玩加电竞   | 英雄联盟场次详细信息爬虫           | wanplus.lol_match_info       | 正常   |
| G-02-1 | WeGame(安卓客户端) | 云顶之弈比赛记录爬虫：召唤师列表   | wegame.tft_summoner_list     | 正常   |
| G-02-2 | WeGame(安卓客户端) | 云顶之弈比赛记录爬虫：游戏场次列表 | wegame.tft_exploit_list      | 正常   |
| G-02-3 | WeGame(安卓客户端) | 云顶之弈比赛记录爬虫：游戏场次详情 | wegame.tft_exploit_detail    | 正常   |
| L-01-1 | 虎牙               | 直播弹幕爬虫                       | huya.barrage_of_live         | 正常   |
| L-01-2 | 虎牙               | 直播间订阅数爬虫                   | huya.subscribe_of_live       | 正常   |
| L-02-1 | 斗鱼               | 直播弹幕爬虫                       | douyu.barrage_of_live        | 正常   |
| L-02-2 | 斗鱼               | 直播间订阅数爬虫                   | douyu.subscribe_of_live      | 待修复 |
| L-03-1 | Bilibili           | 直播弹幕爬虫                       | bilibili.barrage_of_live     | 正常   |
| O-01-1 | 安居客             | 安居客各地房源数量爬虫             | anjuke.housing_resources_num | 正常   |
| O-02-1 | 居理新房           | 居理新房城市页面列表爬虫           | julive.city_url_list         | 正常   |
| O-03-1 | 中国知网           | 期刊包含刊期列表爬虫               | cnki.issue_list              | 正常   |
| O-03-4 | 中国知网           | 刊期包含论文列表爬虫               | cnki.article_list            | 正常   |
| O-04-1 | 猫眼               | 猫眼网播热度爬虫【Demo】           | maoyan.web_heat              | 正常   |
| O-05-1 | 豆瓣               | 豆瓣电影TOP250爬虫                 | douban.movie_top_250         | 正常   |
| N-01-1 | 起点中文网         | 小说排行榜                         | novel.qidian_ranking         | 正常   |

## 爬虫详情

### [S-01-1] 微博热搜榜实时爬虫(weibo.hot_ranking)

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

### [S-02-1] Twitter用户信息爬虫(twitter.user_info)

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

### [S-02-2] Twitter用户推文爬虫(twitter.user_tweet)

> **@author** ChangXing
>
> **@version** 4.1 / 5.1
>
> **@create** 2017.12.30
>
> **@revise** 2020.07.22

采集指定Twitter用户在指定时间范围内表。

* 采集信息：使用Twitter搜索页面进行采集，单一用户的单次采集可追溯数量有限，不宜单次采集过长的时间跨度，可分为多次采集。
* 应用配置：无需使用代理IP，需要使用Selenium

#### V4：过滤用户转推的推文(twitter.user_tweet_v4)

过滤用户转推的推文，仅保留非转推的推文。

| 字段名   | 字段内容           |
| -------- | ------------------ |
| tweet_id | 推文ID             |
| time     | 推文发布时间       |
| text     | 推文内容文本       |
| replies  | 推文回复数         |
| retweets | 推文转推数         |
| likes    | 推文喜欢数(点赞数) |

#### V5：存储用户转推的推文并记录原用户和原推文(twitter.user_tweet_v5)

不过滤用户转推的推文，并记录推文的原用户和原推文

| 字段名       | 字段内容                                             |
| ------------ | ---------------------------------------------------- |
| tweet_id     | 推文ID                                               |
| time         | 推文发布时间                                         |
| text         | 推文内容文本                                         |
| replies      | 推文回复数                                           |
| retweets     | 推文转推数                                           |
| likes        | 推文喜欢数(点赞数)                                   |
| from_user    | 【转推推文】原推文的推文发布者(若非转推推文则为None) |
| from_content | 【转推推文】原推文的推文内容(若非转推推文则为None)   |

### [S-03-1] Facebook用户推文爬虫(facebook.user_tweet)

> **@author** ChangXing
>
> **@version** 4.1
>
> **@create** 2017.12.30
>
> **@revise** 2020.06.08

采集指定Facebook用户在指定时间范围内的推文列表。

* 采集信息：使用Twitter搜索页面进行采集，单一用户的单次采集可追溯数量有限，不宜单次采集过长的时间跨度，可分为多次采集
* 目标Url：https://www.facebook.com/pg/news.ebc/posts/?ref=page_internal
* 推文Url：https://www.facebook.com/news.ebc/posts/2983092458392492
* 应用配置：无需使用代理IP，无需使用Selenium

| 字段名    | 字段内容                   |
| --------- | -------------------------- |
| tweet_id  | 推文ID                     |
| tweet_url | 推文Url                    |
| is_sticky | 推文是否为置顶状态         |
| is_share  | 推文是否为分享             |
| author    | 推文发布者名称             |
| time      | 推文发布时间戳（单位：秒） |
| content   | 推文内容                   |
| reaction  | 推文互动数（即点赞数）     |
| comment   | 推文评论数                 |
| share     | 推文分享数                 |

### [V-01-1] B站UP主发布视频列表爬虫(bilibili.user_video_list)

> **@author** ChangXing
>
> **@version** 1.0
>
> **@create** 2020.05.29

【Demo】采集B站UP主发布视频列表，并输出到控制台。

* 应用配置：无需使用代理IP、无需使用Selenium

### [V-02-1] AcFun视频信息爬虫(acfun.video)

> **@author** ChangXing
>
> **@version** 1.0
>
> **@create** 2020.07.24

采集AcFun视频信息

* 应用配置：无需使用代理IP、无需使用Selenium

| 字段名 | 字段内容     |
| ------ | ------------ |
| title  | 视频标题     |
| videos | 视频下载地址 |

### [G-01-1] WanPlus英雄联盟每日比赛列表爬虫(wanplus.lol_date_list)

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

### [G-01-2] WanPlus英雄联盟比赛包含场次列表爬虫(wanplus.lol_match_list)

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

### [G-01-3] WanPlus英雄联盟场次详细信息爬虫(wanplus.lol_match_info)

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

### [G-02-1] WeGame云顶之弈比赛记录爬虫：召唤师列表(wegame.tft_summoner_list)

> **@author** ChangXing
>
> **@version** 2.1
>
> **@create** 2019.12.10
>
> **@revise** 2020.06.09

使用安卓客户端的API采集WeGame中云顶之弈比赛记录，当前爬虫用于采集高分段召唤师列表。

* 登录状态：需要通过安卓模拟器配合Fiddler抓包获取登录状态（登录状态有24小时左右的有效期）
* 应用配置：无需使用代理IP，无需使用Selenium

### [G-02-2] WeGame云顶之弈比赛记录爬虫：游戏场次列表(wegame.tft_exploit_list)

> **@author** ChangXing
>
> **@version** 2.1
>
> **@create** 2019.12.10
>
> **@revise** 2020.06.09

使用安卓客户端的API采集WeGame中云顶之弈比赛记录，当前爬虫用于依据召唤师列表采集召唤师游戏场次列表。

* 登录状态：需要通过安卓模拟器配合Fiddler抓包获取登录状态（登录状态有24小时左右的有效期）
* 应用配置：无需使用代理IP，无需使用Selenium

### [G-02-3] WeGame云顶之弈比赛记录爬虫：游戏场次详情(wegame.tft_exploit_detail)

> **!!!WeGame数据结构改版，爬虫解析部分可能存在问题!!!**
>
> **@author** ChangXing
>
> **@version** 2.1
>
> **@create** 2019.12.10
>
> **@revise** 2020.06.09

使用安卓客户端的API采集WeGame中云顶之弈比赛记录，当前爬虫用于依据游戏场次列表采集游戏场次详情。

* 登录状态：需要通过安卓模拟器配合Fiddler抓包获取登录状态（登录状态有24小时左右的有效期）

* 应用配置：无需使用代理IP，无需使用Selenium

### [L-01-1] 虎牙直播弹幕爬虫(huya.barrage_of_live)

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

### [L-01-2] 虎牙直播间订阅数爬虫(huya.subscribe_of_live)

>**@author** ChangXing
>
>**@version** 1.2
>
>**@create** 2019.11.24
>
>**@revise** 2020.06.08

依据直播间Url列表，采集列表中直播间的订阅数（暂输出到控制台），Url列表文件中一行一个Url。

* 应用配置：无需使用代理IP，需要使用Selenium

### [L-02-1] 斗鱼直播弹幕爬虫(douyu.barrage_of_live)

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

### [L-02-2] 斗鱼直播间订阅数爬虫(douyu.subscribe_of_live)

>**!!!暂停使用(斗鱼增加字符集反爬，当前抓取结果有误)!!!**
>
>**@author** ChangXing
>
>**@version** 1.2
>
>**@create** 2019.11.24
>
>**@revise** 2020.06.08

依据直播间Url列表，采集列表中直播间的订阅数（暂输出到控制台），Url列表文件中一行一个Url。

* 应用配置：无需使用代理IP，需要使用Selenium

### [L-03-1] Bilibili直播弹幕爬虫(bilibili.barrage_of_live)

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

### [O-01-1] 安居客各地房源数量爬虫(anjuke.housing_resources_num)

> @author: ChangXing
>
> @version: 1.1
>
> @create: 2019.12.17
>
> @revise: 2020.06.09

先采集城市编码列表(crawler_city_list)，再依据城市编码采集城市房源数量(crawler_city_resources)。

* 应用配置：无需使用代理IP，需要使用Selenium

### [O-02-1] 居理新房城市页面列表爬虫(julive.city_url_list)

> @author: ChangXing
>
> @version: 1.1
>
> @create: 2019.12.17
>
> @revise: 2020.06.09

采集各个城市页面的Url列表。

* 应用配置：无需使用代理IP，需要使用Selenium

### [O-03-1] 知网期刊包含刊期列表爬虫(cnki.issue_list)

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

### [O-03-2] 知网刊期包含论文列表爬虫(cnki.article_list)

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

### [O-04-1] 猫眼网播热度(maoyan.web_heat)

> **@author** ChangXing
>
> **@version** 1.0
>
> **@create** 2020.05.26

【Demo】使用Selenium采集猫眼网播热度并输出到控制台。

* 目标Url：http://piaofang.maoyan.com/dashboard/web-heat
* 应用配置：无需使用代理IP、需要使用Selenium

### [O-05-1] 豆瓣电影TOP250爬虫(douban.movie_top_250)

> **@author** ChangXing
>
> **@version** 1.0
>
> **@create** 2020.05.28

采集猫眼网播热度并输出到Json文件。

* 应用配置：无需使用代理IP、无需使用Selenium

# 项目爬虫使用的工具类说明

* crawlertool（必须）：本项目配套的最基本的爬虫工具模块，包括爬虫的抽象基类，以及信息提取、数据库读写、IO操作等工具函数（`pip install crawlertool`）
* Selenium4R（Selenium爬虫必须）：本项目配套的Selenium工具模块，魔改版selenium（`pip install Selenium4R`）
* bs4（beautifulsoup4 ）：部分解析dom页面的爬虫所需的工具模块（`pip install bs4`）
* lxml：部分解析dom页面的爬虫所需的工具模块（`pip install lxml`）

#  爬虫设置调用方法

本合集统一格式的爬虫有三种调用方法：

### （一）在IDE中执行Python脚本

Step 1：安装爬虫运行所需的环境（安装Python环境+pip安装所需的工具模块+安装Chrome浏览器）

Step 2：将爬虫源代码粘贴到IDE

Step 3：参考Demo实现的爬虫结果数据存储

Step 4：运行爬虫

### （二）在命令提示符中执行Python脚本

Step 1：安装爬虫运行所需的环境（安装Python环境+pip安装所需的工具模块+安装Chrome浏览器）

Step 2：在命令提示符（CMD）中使用命令行参数设置并运行爬虫

### （三）使用可执行文件运行（暂未实现）

# 爬虫免责声明

### 1\. 免责声明

* 本合集中所有爬虫仅可用于学习、研究用途，不应用于任何商业用途。
* 本合集所有实现和收录的爬虫均只采集公开显示的数据，如公开显示的数据中包含用户个人数据，将依据学习和研究需要模糊处理。
* 使用者如将本合集中的任何爬虫用于商业用途，后果自负！
* 如本合集中的爬虫对您的权益造成了影响，请联系合集作者，本合集将在24小时内移除该爬虫。

### 2\. 本合集实现爬虫原则

* 严格控制爬虫的请求频率，避免因爬虫导致目标网站的负荷过大。因此，本合集不提供多线程爬虫，同时，在每次请求期间均会留出足够的延时时间。
* 严格控制爬虫仅采集公开的信息。本合集不提供采集被明确标注不希望被他人获取的数据。
* 严格控制爬虫的个人信息获取。爬虫将在抓取环节对于学习、研究无关的个人数据（包括电话、地址、姓名等）进行模糊处理（如记录这些信息的哈希值）。
* 如用户修改或重写爬虫的running方法（即修改或重新设计爬虫），则用户自行设计的爬虫与本合集无关。
* 本合集的的承诺仅对本合集自行实现的爬虫有效，对本合集收录的爬虫，本合集仅作收录，不保证检查其合法性，在使用时，请用户自行衡量并承担其合法性。

# 项目近期计划

1. 使用可执行文件运行爬虫的功能
2. 发布CxSpider模块
3. 用于将爬虫抓取结果（字典列表）存储到不同位置的工具函数（包含于crawlertool工具模块中）
4. 近期准备新增的爬虫

# 项目作者

> **长行** 数据挖掘领域懵逼者
>
> LeetCode主页、Github主页、CSDN主页、有向

本项目诚邀合作开发者，有意者请联系作者的Github账号或邮箱！

# 打赏项目





