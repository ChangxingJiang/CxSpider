from typing import List, Dict

import crawlertool as tool
from Selenium4R import Chrome


class SpiderAnjukeCityCodeList(tool.abc.SingleSpider):
    """
    安居客城市编码列表爬虫

    有效性检验时间 : 2020.12.28
    """

    def __init__(self, driver):
        self.driver = driver

    def running(self) -> List[Dict]:
        self.driver.get("https://www.anjuke.com/sy-city.html")

        result = []
        for city_label in self.driver.find_elements_by_css_selector("body > div.content > div > div.letter_city > ul > li > div > a"):
            city_name = city_label.text
            city_code = city_label.get_attribute("href").replace("https://", "").replace(".anjuke.com/", "")
            result.append({
                "city_name": city_name,
                "city_code": city_code
            })

        return result


if __name__ == "__main__":
    driver = Chrome(cache_path=r"E:\Temp")
    print(SpiderAnjukeCityCodeList(driver).running())
    driver.quit()
