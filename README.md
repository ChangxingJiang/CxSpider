# CxSpider : ChangXing Spider

本项目为爬虫合集，包括作者自行设计实现的爬虫（以下简称合集设计的爬虫），和作者收录的其他爬虫（以下简称爬虫）。其中“合集设计的爬虫”为作者在各种项目中实际使用过的爬虫，至少曾经在某个时刻可以稳定地采集研究量级的数据；“合集收录的爬虫”为作者在任意环境下使用或测试过的爬虫。

因为目标网站随时可能出现变化，同时网站中也可能出现特殊页面，所有爬虫可能出现部分失效或完全失效的情况。因此建议使用者在使用爬虫时仔细检查数据的完整性和准确性，以避免造成损失。

如果您发现本合集中的爬虫出现部分失效或完全失效的情况，请在本项目的[Issues](https://github.com/ChangxingJiang/CxSpider/issues)中提出，谢谢！

-----

* [合集设计的爬虫列表](https://github.com/ChangxingJiang/CxSpider#%E4%B8%80%E5%90%88%E9%9B%86%E8%AE%BE%E8%AE%A1%E7%9A%84%E7%88%AC%E8%99%AB)
* [合集设计的爬虫使用说明](https://github.com/ChangxingJiang/CxSpider#%E4%BA%8C%E7%88%AC%E8%99%AB%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E)
* [合集收录的爬虫列表](https://github.com/ChangxingJiang/CxSpider#%E4%BA%8C%E5%90%88%E9%9B%86%E6%94%B6%E5%BD%95%E7%9A%84%E7%88%AC%E8%99%AB)
* [免责声明](https://github.com/ChangxingJiang/CxSpider#%E4%B8%89%E5%85%8D%E8%B4%A3%E5%A3%B0%E6%98%8E)
* [项目计划](https://github.com/ChangxingJiang/CxSpider#%E5%9B%9B%E9%A1%B9%E7%9B%AE%E8%AE%A1%E5%88%92)
* [项目作者](https://github.com/ChangxingJiang/CxSpider#%E4%BA%94%E9%A1%B9%E7%9B%AE%E4%BD%9C%E8%80%85)

-----

**本合集提醒您：在使用“CxSpider 长行的爬虫合集”（以下简称本合集）的爬虫前，请您务必仔细阅读并透彻理解本合集的[免责声明](https://github.com/ChangxingJiang/CxSpider#%E5%90%88%E9%9B%86%E6%94%B6%E5%BD%95%E7%9A%84%E7%88%AC%E8%99%AB%E5%88%97%E8%A1%A8)（以下简称免责声明）。您可以选择不使用本合集，但如果您使用本合集，您的使用行为将被视为对免责声明全部内容的认可。**

# 一、合集设计的爬虫

“合集设计的爬虫”，即本合集作者自行设计实现的爬虫，这些爬虫均继承了`crawlertool`工具模块中单线程爬虫的抽象基类（`SingleSpider`和`LoopSpider`），具有统一的配置方式、调用方式和返回数据格式。在爬虫具体的设计实现中，为了方便爬虫的使用，遵循了如下原则：

* 每个爬虫为一个单独的Python脚本（.py文件），这个脚本仅依赖于发布在pypi（可以通过pip安装）的工具模块及自身；方便通过直接复制代码来使用爬虫。
* 所有爬虫返回结果均为统一的字典列表格式（`List[Dict]`），同时在工具模块中配有将字典列表格式数据写入到csv、Excel和MySQL的工具函数；方便统一地处理爬虫返回的结果数据。
* 所有爬虫均发布到pypi的`cxspider`模块（`pip install cxspider`）中；方便直接通过pip安装调用。

在使用合集设计的爬虫时，可以结合爬虫的Readme文档以及[”爬虫设置&调用方法“](https://github.com/ChangxingJiang/CxSpider#%E7%88%AC%E8%99%AB%E8%AE%BE%E7%BD%AE%E8%B0%83%E7%94%A8%E6%96%B9%E6%B3%95)中的方法，配置、调用爬虫。

### （一）合集设计的爬虫列表

| 爬虫名称                   | 爬虫平台.爬虫功能 [源代码路径]                               | 爬虫状态 (最近检查时间) |
| -------------------------- | ------------------------------------------------------------ | ----------------------- |
| AcFun_Video                | [A站.视频信息爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Acfun_Video) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Acfun_Video/Acfun_Video.py) | 有效 (2020.12.28)       |
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
| Qidian_Book_Type_List      | [起点中文网.小说排行榜爬虫](https://github.com/ChangxingJiang/CxSpider/tree/master/spider/Qidian_Book_Type_List) [[源]](https://github.com/ChangxingJiang/CxSpider/blob/master/spider/Qidian_Book_Type_List/Qidian_Book_Type_List.py) | 有效 (2020.12.28)       |
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

> **爬虫列表顺序**：先依据域名部分排序，再依据功能部分排序；域名部分按字典序排序，功能部分按功能关系排序。
>
> **爬虫命名规则**：爬虫名称由爬虫目标网站的域名和爬虫的具体功能描述组成。在域名部分中，如果一级域名可以有效描述则包括一级域名即可（例如`AcFun`），如果以及域名不能有效描述，则需要通过“一级域名_二级域名”来表示（例如`Baidu_Tieba`），如果目标为APP，则使用APP的通用名称；一级域名和二级域名均使用驼峰式表示；如果一级域名为数字开头，则在数字前添加大写字母N。在具体功能描述部分中，每个单词都首字母大写，并且使用下划线间隔单词。

###  （二）爬虫使用说明

本项目在计划中将会实现三种运行爬虫的方法，在现阶段在IDE执行Python脚本的运行方法支持较好，未来将会逐渐支持另外两种爬虫的运行方法。

#### 1\. 在IDE中执行Python脚本（当前支持较好）

**第1步：检查Python环境**

> Python版本要求：>=3.8

检查系统的Python环境，如果没有安装则安装Python环境【[教程链接](https://dataartist.blog.csdn.net/article/details/88278970)】；建议同时安装Python的IDE。

**第2步：pip安装爬虫所需的Python工具模块**

每个爬虫依赖的工具模块均在爬虫文档（爬虫文件夹中的README文档）的“依赖列表”中列出，直接使用pip安装即可。一些爬虫经常调用的工具模块的功能如下：

>**crawlertool** : 本项目配套爬虫工具模块 (必需)
>安装：`pip install crawlertool`
>本项目配套的最基本的爬虫工具模块，包括爬虫的抽象基类，以及信息提取、数据库读写、IO操作等工具函数。

>**Selenium4R** : 本项目配套Selenium工具模块 (Selenium爬虫必需)
>安装：`pip install Selenium4R`
>魔改版Selenium，增加webdriver的自动下载和缓存，增加对POST请求的支持，自动处理一些常见异常。

>**bs4 (BeautifulSoup4)** : Dom解析工具 (部分爬虫需要)
>安装：`pip install bs4`

>**lxml** : Dom解析工具 (部分爬虫需要)
>安装：`pip install lxml`

**第3步：安装Chrome浏览器（仅Selenium爬虫需要）**

如果在爬虫文档的“依赖列表”中注明了需要Chrome浏览器，则需要在安装Chrome浏览器【[官网链接](https://www.google.cn/chrome/)】。

**第4步：引用CxSpider项目中的爬虫源代码**

可以通过以下方法引用CxSpider中的爬虫源代码：

* 直接粘贴爬虫源代码中的爬虫类（当前支持较好）

* 安装cxspider模块，引用cxspider模块中的爬虫类（暂未支持）

**第5步：处理爬虫返回的结果数据**

所有爬虫返回的结果数据格式均为列表字典（`List[Dict]`）格式：列表中的每个元素为一条记录（行），单条的记录均为字典格式；字典中的每一个键值对对应记录中的一个字段（列），求中键为字段名，值为字段的值。

本合集设计的爬虫中，对单次运行的爬虫和循环运行的爬虫作出了不同的处理（在爬虫文档中注明了爬虫所属的类型）。具体的：

* 单次运行的爬虫类继承自抽象基类`SingleSpider`，调用爬虫时直接调用爬虫类的`running`方法，`running`方法的返回值即为爬虫返回的结果数据。
* 循环运行的爬虫类继承自抽象基类`LoopSpider`，调用爬虫时调用爬虫的`start`方法即可启动循环运行的爬虫；在每次循环中，爬虫均会将爬虫返回的结果数据作为参数提供给`write`方法，因此需要通过重写`write`方法来处理爬虫返回的结果数据。

**第6步：运行爬虫**

对于单次运行的爬虫，在构造爬虫类后直接调用爬虫类的`running`方法即可；

对于循环运行的爬虫，在构造爬虫类并重写`write`方法后，调用爬虫类的`start`方法即可启动循环运行的爬虫。

#### 2\. 在命令行中执行Python脚本（暂未实现）

**第1步：检查Python环境+pip安装爬虫所需的Python工具模块+安装Chrome浏览器（具体方法同上）**

**第2步：在命令提示符（CMD）中通过命令行参数设置并运行爬虫**

具体命令行参数设置方法将会写在每个爬虫的文档中。

#### 3\. 使用可执行文件运行（暂未实现）

## 二、合集收录的爬虫

“合集收录的爬虫”，即本合集作者在使用后收录的、发布于Github项目或博客中的爬虫。本合集只收录这些爬虫所在的Github项目主页或博客页，具体配置、调用方法及返回数据结构需要使用者自行阅读第三方的爬虫介绍。

本合集可能会将其中部分爬虫整理为本合集的统一格式（即“合集设计的爬虫”的格式），以方便使用者调用，但本合集作者不保证这些整理的准确性、稳定性，请使用者自行衡量。

### 合集收录的爬虫列表

| 爬虫名称 (依据字典顺序排列)   | 爬虫平台.爬虫功能                 | 爬虫地址                                                     |
| ----------------------------- | --------------------------------- | ------------------------------------------------------------ |
| Baidu_Tieba_Tiezi_Post        | 百度贴吧.帖子信息爬虫             | [Github·Tieba_Spider (Aqua-Dream)](https://github.com/Aqua-Dream/Tieba_Spider) |
| Bilibili_Picture              | B站.封面图爬虫                    | [Github·spiders (xiyaowong)](https://github.com/xiyaowong/spiders) |
| DuoWan_LPL_Match_Info         | 多玩游戏.LPL实时比赛信息爬虫      | [Github·Reptile (librauee)](https://github.com/librauee/Reptile) |
| Lagou_Job_Info                | 拉勾网.工作信息爬虫               | [Github·JobSpiders (wqh0109663)](https://github.com/wqh0109663/JobSpiders)<br />[Github·Reptile (librauee)](https://github.com/librauee/Reptile) |
| N51job_Job_Info               | 前程无忧.工作信息爬虫             | [Github·JobSpiders (wqh0109663)](https://github.com/wqh0109663/JobSpiders) |
| NowCoder_Interview_Experience | 牛客网.面经爬虫                   | [Github·Reptile (librauee)](https://github.com/librauee/Reptile) |
| Toutiao_Search_List           | 今日头条·头条搜索爬虫             | [Giuthub·TTBot (01ly)](https://github.com/01ly/TTBot)        |
| Toutiao_News_List             | 今日头条·新闻列表爬虫(45个类别)   | [Giuthub·TTBot (01ly)](https://github.com/01ly/TTBot)        |
| Toutiao_User_Info             | 今日头条·账号信息爬虫             | [Giuthub·TTBot (01ly)](https://github.com/01ly/TTBot)        |
| Toutiao_User_Post             | 今日头条·账号发布文章爬虫         | [Giuthub·TTBot (01ly)](https://github.com/01ly/TTBot)        |
| Toutiao_User_Video            | 今日头条·账号发布视频爬虫         | [Giuthub·TTBot (01ly)](https://github.com/01ly/TTBot)        |
| WeChat_Account_Info           | 微信公众号.公众号信息爬虫         | [Github·wechat-spider (striver-ing)](https://github.com/striver-ing/wechat-spider) |
| WeChat_Article_List           | 微信公众号.公众号文章列表爬虫     | [Github·wechat-spider (striver-ing)](https://github.com/striver-ing/wechat-spider) |
| WeChat_Article_Info           | 微信公众号.公众号文章信息爬虫     | [Github·wechat-spider (striver-ing)](https://github.com/striver-ing/wechat-spider) |
| WeChat_Article_Comment        | 微信公众号.公众号文章评论爬虫     | [Github·wechat-spider (striver-ing)](https://github.com/striver-ing/wechat-spider) |
| Weibo_User_Info               | 微博.账号信息爬虫                 | [Github·WeiboSpider (nghuyong)](https://github.com/nghuyong/WeiboSpider) |
| Weibo_User_Post               | 微博.账号发布推文爬虫             | [Github·WeiboSpider (nghuyong)](https://github.com/nghuyong/WeiboSpider) |
| Weibo_Social_Network          | 微博.账号社交关系爬虫             | [Github·WeiboSpider (nghuyong)](https://github.com/nghuyong/WeiboSpider) |
| Weibo_Post_Comment            | 微博.微博评论爬虫                 | [Github·WeiboSpider (nghuyong)](https://github.com/nghuyong/WeiboSpider) |
| Weibo_Post_By_Keyword         | 微博.基于关键词和时间段的微博爬虫 | [Github·WeiboSpider (nghuyong)](https://github.com/nghuyong/WeiboSpider) |
| Zhaopin_Job_Info              | 智联招聘.工作信息爬虫             | [Github·JobSpiders (wqh0109663)](https://github.com/wqh0109663/JobSpiders) |

> **爬虫列表顺序 / 爬虫命名规则**：与[“合集设计的爬虫列表”的命名规则](https://github.com/ChangxingJiang/CxSpider#%E4%B8%80%E5%90%88%E9%9B%86%E8%AE%BE%E8%AE%A1%E7%9A%84%E7%88%AC%E8%99%AB%E5%88%97%E8%A1%A8)相同。

## 三、免责声明

### （一）针对合集设计的爬虫 (“合集设计的爬虫列表”中的爬虫)

1\. 所有本合集设计的爬虫均仅可用于研究和教学用途，不得用于任何商业用途。使用者如将任何本合集设计的爬虫应用于商业用途，则由使用者自行衡量其合法性，并承担相关的法律责任。

2\. 所有本合集设计的爬虫均作出了如下限制：

* 严格控制请求频率；
* 严格限制仅采集公开、没有被标注为不希望他人获取的数据；
* 严格模糊处理与研究和教学无关的个人数据（如姓名、电话、地址等），使其只能用于区分，而无实际意义（采用哈希方法）；

使用者如通过修改爬虫代码（修改爬虫类的running方法）的方法以绕过以上限制，则由使用者自行并承担相关的法律责任。

3\. 使用者如在本合集爬虫的基础上重新设计爬虫（即修改或重写爬虫的running方法），则重新设计的爬虫与本合集无关，由使用者自行承担相关的法律责任。

4\. 任何单位或个人认为本合集的任何爬虫可能涉嫌侵犯其权益，可联系本合集作者，本合集将在24小时内移除该爬虫。

### （二）针对合集收录的爬虫 (“合集收录的爬虫列表”中的爬虫)

1\. 本合集收录的第三方爬虫均系他人制作或提供，您可能从该爬虫的网页上获得目标爬虫，本合集对其合法性概不负责，亦不承担任何法律责任。

2\. 本合集将收录的部分第三方爬虫改写为本合集的统一格式（即“合集设计的爬虫”的格式），以方便使用者调用，这些被改写的新爬虫将适用于“针对合集设计的爬虫”的免责声明；同时，“合集收录的爬虫列表”中的第三方爬虫仍适用于“针对合集收录的爬虫”的免责声明。

3\. 任何单位或个人认为本合集链接到的第三方网页内容可能涉嫌侵犯其信息网络传播权，可联系本合集作者，本合集将尽快断开相关链接内容。

## 四、项目计划

### （一）项目计划

#### 1\. 计划完成的项目更新

* 在crawlertool爬虫工具模块中，实现将统一的爬虫返回数据格式（字典列表）存储到不同位置的工具函数
* 整理CxSpider模块并发布到pypi
* 实现爬虫调用的命令行参数支持
* 实现通过不需要本地Python环境的可执行文件运行爬虫（按爬虫分别封装/封装通用的爬虫调用器）
* 更新webdriver的管理方式，不再需要用户再管理缓存路径

#### 2\. 计划新增的爬虫

* 大众点评商铺数据：商铺名称、商铺地址、联系方式、五星好评、人均、环境、音效、服务（@**[MrLuoj](https://github.com/MrLuoj)**）
* WeGame：指定名称召唤师的匹配或排位记录（@**[ixuhan](https://github.com/ixuhan)**）
* Twitter：目标用户发布的图片及视频

### （二）项目历史

2021.01.02 整体整理、更新项目结构

2020.11.01 达到100☆

2020.06.09 迁移、合并合集作者的另外几个爬虫项目

## 五、项目作者

> **长行** · [Github](https://github.com/ChangxingJiang) · [CSDN](https://blog.csdn.net/Changxing_J) · [LeetCode](https://leetcode-cn.com/u/changxingjiang/) · 1278729001@qq.com

诚邀对爬虫感兴趣的朋友共同维护此项目，有意者请联系作者的Github账号或邮箱！

