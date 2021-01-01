# AcFun视频信息爬虫（包括下载地址）

> 最新有效性检查时间：2020.10.18

#### 参数

* page_url：视频页面地址

#### 所需第三方包

* Utils4R >= 0.0.6

#### 返回数据结果

```json
{
	'视频标题': '这床真香！【紫颜】',
	'视频下载地址': 'http://tx-safety-video.acfun.cn/mediacloud/acfun/acfun_video/BEI7FLXo9B-3APsUS5me1SI_ARzJ3xSHKGF_swFZ03UGhHN3W3-W6K6GvzH1Yyps.mp4?pkey=AAI6StIzW0mvB760uxP4-6xrKNC3v6zdcbL5NmpdnWPHVkX0k_MyclVvcWNGsjj4QZD9MThVr241kjtyB9KFjkCk3quzb7uc8KZ8MtNEr5SxbHiC3-VtdkUUkyKnFkH6jPJB_mWSRaUqbRhrgiDpa7w1jRgfteT1eneYnwHxaIVUzrAIvzbTtPwFVPf2b0do0DYkdRsveJvxckfamTHEZ3AAf0t-jZt9vY1rDlTSD8uwx9v-pg0Zo88rw5qSmxCFOSh4mLtJytBf0C7ABqWdYCqS_gx2PAE1Y9DsMsAdPTn3fQ'
}
```

#### 调用Demo

```python
spider = Spider()
print(spider.run(page_url="https://www.acfun.cn/v/ac16986343"))
```



### [V-02-1] AcFun视频信息爬虫(acfun.video)

> **@author** ChangXing
>
> **@version** 1.0
>
> **@create** 2020.07.24

采集AcFun视频信息

* 应用配置：无需使用代理IP、无需使用Selenium

| 字段名 | 字段内容     |
| ------ | ------------ |
| title  | 视频标题     |
| videos | 视频下载地址 |

### 