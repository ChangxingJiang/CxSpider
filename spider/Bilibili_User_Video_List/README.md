### B站UP主发布视频列表爬虫(bilibili.user_video_list)

> **@author** ChangXing
>
> **@version** 1.0
>
> **@create** 2020.05.29

【Demo】采集B站UP主发布视频列表，并输出到控制台。

* 应用配置：无需使用代理IP、无需使用Selenium

# B站UP主发布视频列表爬虫

> 最新有效性检查时间：2020.10.18

#### 所需第三方包

* Utils4R >= 0.0.6
* requests >= 2.23.0

#### 调用Demo

```python
spider = SpiderBilibiliUserVideoList()
print(spider.run(20165629))  # 其中20165629为用户ID
```



