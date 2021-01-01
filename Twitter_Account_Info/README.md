### Twitter用户信息爬虫(twitter.user_info)

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