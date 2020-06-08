from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import environment as env


def open_chrome():
    """ 启动Chrome浏览器

    :return <selenium.webdriver.chrome.webdriver.WebDriver> Chrome浏览器对象
    """

    chrome_options = Options()  # 启动Chrome浏览器设置对象

    # 设置Chrome用户文件信息(使用Chrome浏览器中已登录的Google账号打开Selenium控制的Chrome浏览器)
    chrome_options.add_argument("user-data-dir=" + env.CHROME_USERDATA_PATH)

    # 设置Chrome浏览器可执行文件路径(如果Selenium控制的Chrome浏览器启动报错则取消这行的注释)
    # chrome_options.binary_location = env.CHROME_LOCATION

    # 设置浏览器下载文件存储路径
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": env.CHROME_DOWNLOAD_PATH,  # 设置下载文件的存储路径
        "download.prompt_for_download": False,  # 设置下载文件是否弹出窗口
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,  # 控制打开新标签页是否使处于后台的Chrome窗口被激活
    })

    # 启动Chrome浏览器
    return webdriver.Chrome(options=chrome_options, executable_path=env.CHROMEDRIVER_PATH)


if __name__ == "__main__":
    pass
