### Facebook用户推文爬虫(facebook.user_tweet)

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

### 