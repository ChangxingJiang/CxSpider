# WanPlus英雄联盟每日比赛列表爬虫文档

> 最新有效性检查时间：2020.12.28

**爬虫类型**：单次运行爬虫

**爬虫依赖第三方模块**：crawlertool

**爬虫功能**：采集WanPlus英雄联盟每日比赛列表

* 目标Url：https://www.wanplus.com/lol/schedule
* 实际请求的Ajax：https://www.wanplus.com/ajax/schedule/list

**爬虫参数**：

| 参数名     | 参数功能                       |
| ---------- | ------------------------------ |
| start_date | 抓取范围开始日期（最早的日期） |
| end_date   | 抓取范围结束日期（最晚的日期） |

**爬虫返回结果数据**：

| 字段名           | 字段内容                             |
| ---------------- | ------------------------------------ |
| date             | 日期                                 |
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

**创建时间**：2020.04.20

**修改时间**：2020.12.28