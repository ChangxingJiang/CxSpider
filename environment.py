import json

# 读取爬虫环境高配置文件
SETTING_PATH = r"E:\【微云工作台】\环境配置\爬虫环境配置.json"  # 爬虫环境配置文件路径
with open(SETTING_PATH, "r", encoding="UTF-8") as f:
    setting = json.loads(f.read())

# 读取代理IP相关设置
PROXY_BELONG = None  # 代理IP:所属公司
PROXY_API = None  # 代理IP:API的Url
if "Proxy IP" in setting and setting["Proxy IP"] is not None:
    if "Belong" in setting["Proxy IP"]:
        PROXY_BELONG = setting["Proxy IP"]["Belong"]
    if "Ajax Url" in setting["Proxy IP"]:
        PROXY_API = setting["Proxy IP"]["Ajax Url"]

# 读取Selenium相关设置
CHROMEDRIVER_PATH = None  # ChromeDriver可执行文件路径
CHROME_LOCATION = None  # Chrome浏览器可执行文件路径
CHROME_USERDATA_PATH = None  # Chrome浏览器用户数据文件夹路径
CHROME_DOWNLOAD_PATH = None  # Chrome浏览器下载文件存储路径
if "ChromeDriver" in setting and setting["ChromeDriver"] is not None:
    if "Executable Path" in setting["ChromeDriver"]:
        CHROMEDRIVER_PATH = setting["ChromeDriver"]["Executable Path"]
    if "Chrome Location" in setting["ChromeDriver"]:
        CHROME_LOCATION = setting["ChromeDriver"]["Chrome Location"]
    if "Chrome User Data Path" in setting["ChromeDriver"]:
        CHROME_USERDATA_PATH = setting["ChromeDriver"]["Chrome User Data Path"]

# 读取MySQL相关设置
MYSQL_INFO = dict()
if "MySQL" in setting and setting["MySQL"] is not None:
    MYSQL_INFO = setting["MySQL"]

# 读取爬虫相关数据
DATA = dict()
if "Data" in setting and setting["Data"] is not None:
    DATA = setting["Data"]

# 读取路径相关数据
PATH = dict()
if "Path" in setting and setting["Path"] is not None:
    PATH = setting["Path"]
