### 虎牙直播弹幕爬虫(huya.barrage_of_live)

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