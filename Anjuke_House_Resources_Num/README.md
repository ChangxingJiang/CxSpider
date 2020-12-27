# 安居客各地房源数量爬虫

> 最新有效性检查时间：2020.10.18

#### 所需第三方包

* Selenium4R >= 0.0.3
* Utils4R >= 0.0.6

#### 运行说明

先采集城市编码列表，生成城市名称和城市编码的对应表；然后再使用这个对应表逐个采集各个城市的房源你数量。

#### 调用Demo

```python
driver = Chrome(cache_path=r"E:\Temp")

# 采集城市编码列表
spider_city_code = SpiderCityCode(driver)
result1 = spider_city_code.run()
Utils.io.write_json("anjuke_city_code.json", result1)

# 采集城市房源数量
city_code_list = Utils.io.load_json("anjuke_city_code.json")
city_info_list = Utils.io.load_json("anjuke_city_infor.json", default={})
spider_city_info = SpiderCityInfo(driver)
for city_name, city_code in city_code_list.items():
    if city_name not in city_info_list:
        city_info_list[city_name] = spider_city_info.run(city_code=city_code)
        Utils.io.write_json("anjuke_city_info.json", city_info_list)
        time.sleep(2)

driver.quit()
```

