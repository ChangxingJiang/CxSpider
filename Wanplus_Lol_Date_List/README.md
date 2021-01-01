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

### 