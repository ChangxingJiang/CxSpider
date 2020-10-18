# CNKI(中国知网)期刊刊期列表爬虫

> 最新有效性检查时间：2020.10.18

#### 所需第三方包

* requests >= 2.23.0
* BeautifulSoup4 >= 4.9.0
* Utils4R >= 0.0.6

#### 调用Demo

```python
journal_list = {
    "CSSCI-新闻与传播学": [
        ["新闻与传播研究", "CJFD", "YANJ"],
        ["编辑学报", "CJFD", "BJXB"],
        ["编辑之友", "CJFD", "BJZY"],
        ["出版发行研究", "CJFD", "CBFX"],
        ["出版科学", "CJFD", "CBKX"],
        ["当代传播", "CJFD", "DACB"],
        ["国际新闻界", "CJFD", "GJXW"],
        ["科技与出版", "CJFD", "KJYU"],
        ["现代出版", "CJFD", "DXCB"],
        ["现代传播(中国传媒大学学报)", "CJFD", "XDCB"],
        ["新闻大学", "CJFD", "XWDX"],
        ["新闻记者", "CJFD", "XWJZ"],
        ["新闻界", "CJFD", "NEWS"],
        ["中国出版", "CJFD", "ZGCB"],
        ["中国科技期刊研究", "CJFD", "JYKQ"]
    ],
    "CSSCI扩展-新闻与传播学": [
        ["编辑学刊", "CJFD", "BJXZ"],
        ["出版广角", "CJFD", "CBGJ"],
        ["传媒", "CJFD", "CMEI"],
        ["电视研究", "CJFD", "DSYI"],
        ["全球传媒学刊", "CJFD", "QQCM"],
        ["新闻爱好者", "CJFD", "XWAH"],
        ["新闻与传播评论", "CJFD", "WHDS"],
        ["新闻与写作", "CJFD", "XWXZ"],
        ["中国编辑", "CJFD", "BJZG"]
    ]
}

spider = SpiderCnkiIssueList()
for journal in journal_list["CSSCI-新闻与传播学"]:
    print(journal[0], ":", spider.run(journal[1], journal[2]))
```

# CNKI(中国知网)期刊刊期列表爬虫

> 最新有效性检查时间：2020.10.18

#### 所需第三方包

* requests >= 2.23.0
* BeautifulSoup4 >= 4.9.0
* Utils4R >= 0.0.6

#### 调用Demo

```python
spider_cnki_issue_list = SpiderCnkiIssueList()
for journal in journal_list["CSSCI-新闻与传播学"]:
    print(journal[0], ":", spider_cnki_issue_list.run(journal[1], journal[2]))
```