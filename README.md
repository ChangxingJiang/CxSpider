# CxSpider : ChangXing Spider

本项目为爬虫合集，包括作者自行设计实现的爬虫（以下简称合集设计的爬虫），和作者收录的其他爬虫（以下简称爬虫）。

**本合集提醒您：在使用“CxSpider 长行的爬虫合集”（以下简称本合集）的爬虫前，请您务必仔细阅读并透彻理解本合集的[免责声明](https://github.com/ChangxingJiang/CxSpider#%E5%90%88%E9%9B%86%E6%94%B6%E5%BD%95%E7%9A%84%E7%88%AC%E8%99%AB%E5%88%97%E8%A1%A8)（以下简称免责声明）。您可以选择不使用本合集，但如果您使用本合集，您的使用行为将被视为对免责声明全部内容的认可。**

### 目录

* [合集设计的爬虫](https://github.com/ChangxingJiang/CxSpider#%E5%90%88%E9%9B%86%E8%AE%BE%E8%AE%A1%E7%9A%84%E7%88%AC%E8%99%AB)
  * [爬虫列表](https://github.com/ChangxingJiang/CxSpider#%E5%90%88%E9%9B%86%E8%AE%BE%E8%AE%A1%E7%9A%84%E7%88%AC%E8%99%AB%E5%88%97%E8%A1%A8)
  * [爬虫的设置&调用方法](https://github.com/ChangxingJiang/CxSpider#%E7%88%AC%E8%99%AB%E8%AE%BE%E7%BD%AE%E8%B0%83%E7%94%A8%E6%96%B9%E6%B3%95)
  * [工具类说明](https://github.com/ChangxingJiang/CxSpider#%E5%B7%A5%E5%85%B7%E7%B1%BB%E8%AF%B4%E6%98%8E)
* [合集收录的爬虫](https://github.com/ChangxingJiang/CxSpider#%E5%90%88%E9%9B%86%E6%94%B6%E5%BD%95%E7%9A%84%E7%88%AC%E8%99%AB)
  * [爬虫列表](https://github.com/ChangxingJiang/CxSpider#%E5%90%88%E9%9B%86%E6%94%B6%E5%BD%95%E7%9A%84%E7%88%AC%E8%99%AB%E5%88%97%E8%A1%A8)
* [免责声明](https://github.com/ChangxingJiang/CxSpider#%E5%90%88%E9%9B%86%E6%94%B6%E5%BD%95%E7%9A%84%E7%88%AC%E8%99%AB%E5%88%97%E8%A1%A8)
* 爬虫相关答疑
* [项目近期计划](https://github.com/ChangxingJiang/CxSpider#%E9%A1%B9%E7%9B%AE%E8%BF%91%E6%9C%9F%E8%AE%A1%E5%88%92)
* [项目作者介绍](https://github.com/ChangxingJiang/CxSpider#%E9%A1%B9%E7%9B%AE%E4%BD%9C%E8%80%85%E4%BB%8B%E7%BB%8D)

# 合集设计的爬虫

对于本合集自行设计实现的爬虫，本合集统一了爬虫的配置方式、调用方式和返回结果格式，在设计中遵循如下原则：

1. 每个Python脚本（.py文件）仅依赖于发布在pypi（可以通过pip安装）的工具即自身，方便直接复制代码来使用爬虫。
2. 爬虫返回结果统一为字典列表格式，并在工具类中配有将这种格式写入csv、Excel和MySQL的工具函数。
3. 将所有爬虫发布到pypi的cxspider模块（`pip install cxspider`），方便直接调用。

## 合集设计的爬虫列表

**爬虫顺序**：爬虫目标网站的一级域名的首字母顺序。

**爬虫命名规则**：爬虫名称由爬虫目标网站的一级域名（例如`AcFun`）和爬虫的具体功能描述（例如`Video`）组成；其中，一级域名内部使用驼峰式表示，具体功能描述用下划线间隔单词，每个被下划线分隔的单词均首字母大写。

| 爬虫名称                   | 爬虫平台.爬虫功能 [源代码路径]                               | 爬虫状态 (最近检查时间) |
| -------------------------- | ------------------------------------------------------------ | ----------------------- |
| AcFun_Video                | [A站.视频信息爬虫(包括下载地址)](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Acfun_Video) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Acfun_Video/Acfun_Video.py) | 有效 (2020.12.28)       |
| Alexa_Website_Info         | [Alexa.网站信息爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Alexa_Website_Info) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Alexa_Website_Info/Alexa_Website_Info.py) | 有效 (2020.12.28)       |
| Anjuke_City_Code_List      | [安居客.各城市编码列表爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Anjuke_City_Code_List) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Anjuke_City_Code_List/Anjuke_City_Code_List.py) | 有效 (2020.12.28)       |
| Anjuke_House_Resources_Num | [安居客.房源数量爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Anjuke_House_Resources_Num) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Anjuke_House_Resources_Num/Anjuke_House_Resources_Num.py) | 有效 (2020.12.28)       |
| Bilibili_Live_Barrage      | [B站.直播弹幕爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Bilibili_Live_Barrage) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Bilibili_Live_Barrage/Bilibili_Live_Barrage.py) | 有效 (2020.12.28)       |
| Bilibili_User_Video_List   | [B站.UP主发布视频列表爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Bilibili_User_Video_List) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Bilibili_User_Video_List/Bilibili_User_Video_List.py) | 有效 (2020.12.28)       |
| Cnki_Article_List          | [中国知网.刊期包含论文列表爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Cnki_Article_List) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Cnki_Article_List/Cnki_Article_List.py) | 有效 (2020.12.28)       |
| Cnki_Issue_List            | [中国知网.期刊包含刊期列表爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Cnki_Issue_List) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Cnki_Issue_List/Cnki_Issue_List.py) | 有效 (2020.12.28)       |
| Douban_Movie_Top_250       | [豆瓣.电影TOP250爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Douban_Movie_Top_250) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Douban_Movie_Top_250/Douban_Movie_Top_250.py) | 有效 (2020.12.28)       |
| Douyu_Live_Barrage         | [斗鱼.直播弹幕爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Douyu_Live_Barrage) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Douyu_Live_Barrage/Douyu_Live_Barrage.py) | 有效 (2020.12.28)       |
| Douyu_Live_Subscribe       | [斗鱼.直播间订阅数爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Douyu_Live_Subscribe) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Douyu_Live_Subscribe/Douyu_Live_Subscribe.py) | 已失效                  |
| Facebook_Account_Info      | [Facebook.账号信息爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Facebook_Account_Info) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Facebook_Account_Info/Facebook_Account_Info.py) | 有效 (2020.12.28)       |
| Facebook_Account_Post      | [Facebook.账号发布推文爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Facebook_Account_Post) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Facebook_Account_Post/Facebook_Account_Post.py) | 有效 (2020.12.28)       |
| Google_Result_Num          | [Google.搜索结果数量爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Google_Result_Num) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Google_Result_Num/Google_Result_Num.py) | 有效 (2020.12.28)       |
| Huya_Live_Barrage          | [虎牙.直播弹幕爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Huya_Live_Barrage) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Huya_Live_Barrage/Huya_Live_Barrage.py) | 已失效                  |
| Huya_Live_Subscribe        | [虎牙.直播间订阅数爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Huya_Live_Subscribe) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Huya_Live_Subscribe/Huya_Live_Subscribe.py) | 有效 (2020.12.28)       |
| Julive_City_Url_List       | [居理新房.城市页面地址列表爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Julive_City_Url_List) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Julive_City_Url_List/Julive_City_Url_List.py) | 有效 (2020.12.28)       |
| Maoyan_Web_Heat            | [猫眼.猫眼网播热度爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Maoyan_Web_Heat) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Maoyan_Web_Heat/Maoyan_Web_Heat.py) | 有效 (2020.12.28)       |
| Qidian_Book_Type_List      | [起点中文网.小说排行榜](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Qidian_Book_Type_List) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Qidian_Book_Type_List/Qidian_Book_Type_List.py) | 有效 (2020.12.28)       |
| Twitter_Account_Info       | [Twitter.账号信息爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Twitter_Account_Info) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Twitter_Account_Info/Twitter_Account_Info.py) | 有效 (2020.12.28)       |
| Twitter_Account_Post       | [Twitter.账号发布推文爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Twitter_Account_Post) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Twitter_Account_Post/Twitter_Account_Post.py) | 有效 (2020.12.28)       |
| Wanplus_Lol_Date_List      | [玩加电竞.英雄联盟每日比赛列表爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Wanplus_Lol_Date_List) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Wanplus_Lol_Date_List/Wanplus_Lol_Date_List.py) | 有效 (2020.12.28)       |
| Wanplus_Lol_Match_Info     | [玩加电竞.英雄联盟场次详细信息爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Wanplus_Lol_Match_Info) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Wanplus_Lol_Match_Info/Wanplus_Lol_Match_Info.py) | 已失效                  |
| Wanplus_Lol_Match_List     | [玩加电竞.英雄联盟比赛包含场次列表爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Wanplus_Lol_Match_List) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Wanplus_Lol_Match_List/Wanplus_Lol_Match_List.py) | 有效 (2020.12.28)       |
| WeGame_TFT_Exploit_Detail  | [WeGame.云顶之弈比赛记录爬虫C:游戏场次详情](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/WeGame_TFT_Exploit_Detail) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/WeGame_TFT_Exploit_Detail/WeGame_TFT_Exploit_Detail.py) | 有效 (2020.01.08)       |
| WeGame_TFT_Exploit_List    | [WeGame.云顶之弈比赛记录爬虫B:游戏场次列表](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/WeGame_TFT_Exploit_List) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/WeGame_TFT_Exploit_List/WeGame_TFT_Exploit_List.py) | 有效 (2020.01.08)       |
| WeGame_TFT_Summoner_List   | [WeGame.云顶之弈比赛记录爬虫A:召唤师列表](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/WeGame_TFT_Summoner_List) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/WeGame_TFT_Summoner_List/WeGame_TFT_Summoner_List.py) | 有效 (2020.01.08)       |
| Weibo_Account_Info         | [微博.账号信息爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Weibo_Account_Info) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Weibo_Account_Info/Weibo_Account_Info.py) | 有效 (2020.12.28)       |
| Weibo_Account_Post         | [微博.账号发布推文爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Weibo_Account_Post) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Weibo_Account_Post/Weibo_Account_Post.py) | 有效 (2020.12.28)       |
| Weibo_Hot_Ranking          | [微博.热搜榜爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Weibo_Hot_Ranking) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Weibo_Hot_Ranking/Weibo_Hot_Ranking.py) | 有效 (2020.12.28)       |

##  爬虫设置&调用方法

本合集统一格式的爬虫有三种调用方法：

#### （一）在IDE中执行Python脚本

Step 1：安装爬虫运行所需的环境（安装Python环境+pip安装所需的工具模块+安装Chrome浏览器）

Step 2：将爬虫源代码粘贴到IDE

Step 3：参考Demo实现的爬虫结果数据存储

Step 4：运行爬虫

#### （二）在命令提示符中执行Python脚本

Step 1：安装爬虫运行所需的环境（安装Python环境+pip安装所需的工具模块+安装Chrome浏览器）

Step 2：在命令提示符（CMD）中使用命令行参数设置并运行爬虫

#### （三）使用可执行文件运行（暂未实现）

#### （四）返回数据格式说明

## 工具类说明

* crawlertool（必须）：本项目配套的最基本的爬虫工具模块，包括爬虫的抽象基类，以及信息提取、数据库读写、IO操作等工具函数（`pip install crawlertool`）
* Selenium4R（Selenium爬虫必须）：本项目配套的Selenium工具模块，魔改版selenium（`pip install Selenium4R`）
* bs4（beautifulsoup4 ）：部分解析dom页面的爬虫所需的工具模块（`pip install bs4`）
* lxml：部分解析dom页面的爬虫所需的工具模块（`pip install lxml`）

> 所有爬虫均会在自己的说明（`README.md`）中注明该爬虫所需的工具模块。

# 合集收录的爬虫

对于本合集收录的爬虫，均为发布在Github或博客中的爬虫，本项目作者测试基本无误后收录。本合集将其中的部分爬虫改变为本合集的统一格式，以方便调用，但会明确标注爬虫的来源。

## 合集收录的爬虫列表

# 免责声明

#### （一）针对合集设计的爬虫 (“合集设计的爬虫列表”中的爬虫)

1\. 所有本合集设计的爬虫均仅可用于研究和教学用途，不得用于任何商业用途。使用者如将任何本合集设计的爬虫应用于商业用途，则由使用者自行衡量其合法性，并承担相关的法律责任。

2\. 所有本合集设计的爬虫均作出了如下限制：

* 严格控制请求频率；
* 严格限制仅采集公开、没有被标注为不希望他人获取的数据；
* 严格模糊处理与研究和教学无关的个人数据（如姓名、电话、地址等），使其只能用于区分，而无实际意义（采用哈希方法）；

使用者如通过修改爬虫代码（修改爬虫类的running方法）的方法以绕过以上限制，则由使用者自行并承担相关的法律责任。

3\. 使用者如在本合集爬虫的基础上重新设计爬虫（即修改或重写爬虫的running方法），则重新设计的爬虫与本合集无关，由使用者自行承担相关的法律责任。

4\. 任何单位或个人认为本合集的任何爬虫可能涉嫌侵犯其权益，可联系本合集作者，本合集将会尽快移除该爬虫。

#### （二）针对合集收录的爬虫 (“合集收录的爬虫列表”中的爬虫)

* 本合集收录的第三方爬虫均系他人制作或提供，您可能从该爬虫的网页上获得目标爬虫，本合集对其合法性概不负责，亦不承担任何法律责任。

* 任何单位或个人认为本合集链接到的第三方网页内容可能涉嫌侵犯其信息网络传播权，可联系本合集作者，本合集将尽快断开相关链接内容。

# 项目近期计划

1. 使用可执行文件运行爬虫的功能
2. 发布CxSpider模块
3. 用于将爬虫抓取结果（字典列表）存储到不同位置的工具函数（包含于crawlertool工具模块中）
4. 近期准备新增的爬虫

# 项目作者介绍

> **长行** 数据挖掘领域懵逼者
>
> LeetCode主页、Github主页、CSDN主页、邮箱

本项目诚邀合作开发者，有意者请联系作者的Github账号或邮箱！

### 打赏项目





