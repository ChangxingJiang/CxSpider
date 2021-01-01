### 知网刊期包含论文列表爬虫(cnki.article_list)

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

### 