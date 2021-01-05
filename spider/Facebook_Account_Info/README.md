# Facebook账号信息爬虫文档

> 最新有效性检查时间：2020.12.28

**爬虫类型**：单次运行爬虫

**爬虫依赖第三方模块**：crawlertool、Selenium4R

**爬虫功能**：采集Facebook账号的基本信息

适用于Facebook老版本UI(FB4)的Facebook账号信息爬虫。

**爬虫参数**：

| 参数名   | 参数功能                                                     |
| -------- | ------------------------------------------------------------ |
| page_url | Facebook账号主页Url（形如：https://www.facebook.com/zaobaosg/） |

**爬虫返回结果数据**：

| 字段名     | 字段内容             |
| ---------- | -------------------- |
| account_id | Facebook账号唯一ID   |
| follow     | Facebook账号的粉丝数 |
| favor      | Facebook账号的点赞数 |

**创建时间**：2017.12.30

**修改时间**：2020.12.28

