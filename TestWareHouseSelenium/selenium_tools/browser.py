from typing import Union, Type
from selenium.webdriver import *
from selenium.webdriver.opera.options import Options as OperaOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

BROWSERS = (Chrome, Ie, Firefox, Edge, Opera, PhantomJS)
OPTIONS = (ChromeOptions, IeOptions, FirefoxOptions, EdgeOptions, OperaOptions)


class BROWSER:

    CHROME_DRIVER_PATH = "C:/temp/chrome_driver/chromedriver.exe"

    # 使用32位ie驱动解决文本输入缓慢的问题
    #IE_DRIVER_PATH = IE_DRIVER_PATH

    #FIREFOX_DRIVER_PATH = FIREFOX_DRIVER_PATH
    #EDGE_DRIVER_PATH = EDGE_DRIVER_PATH
    #OPERA_DRIVER_PATH = OPERA_DRIVER_PATH

    HEADLESS = True

    # IMPLICITLY WAITING TIME METHOD
    IMPLICITLY_WAIT_TIME = 10

    # PAGE SOURCE LOAD TIME METHOD
    PAGE_LOAD_TIME = 10

    # the script should wait during an
    # execute_async_script call before throwing an error
    SCRIPT_TIMEOUT = 0

    # SET WINDOW SIZE METHOD
    WINDOWS_SIZE = (1024, 900)

    def __init__(self, browser_type: Type[Union[Chrome, Ie, Firefox, Edge, Opera, PhantomJS, Remote]] = Chrome,
                 option_type: Type[Union[FirefoxOptions, ChromeOptions, IeOptions, EdgeOptions, OperaOptions]] = ChromeOptions,
                 driver_path: str = CHROME_DRIVER_PATH):
        if not issubclass(browser_type, BROWSERS):
            raise TypeError
        if not issubclass(option_type, OPTIONS):
            raise TypeError
        if not isinstance(driver_path, str):
            raise TypeError
        self._driver = browser_type
        self._option = option_type
        self._path = driver_path

    @property
    def browser(self):
        """
        subclass should implement this method
        return the instance of WebDriver
        :return:
        """
        return

    @property
    def _options(self):
        """
        subclass should implement this method
        return instance of the Option Type like ChromeOptions
        :return:
        """
        return


class CHROME(BROWSER):

    METHOD_MARK = True

    IMPLICITLY_WAIT_TIME = 30

    PAGE_LOAD_TIME = 20

    SCRIPT_TIMEOUT = 10

    # HEADLESS MODEL OPTION
    HEADLESS = False

    OPTION_MARK = True

    # EXPERIMENTAL OPTION
    EXPERIMENTAL = {
         #'mobileEmulation': {'deviceName': 'iPhone 6'},#以移动方式打开
        'excludeSwitches': ['enable-automation']#不显示“正在接受自动程序控制”
    }

    # WINDOW SIZE OPTION
    WINDOW_SIZE = ''
    # WINDOW_SIZE = '--window-size=1920,1080'

    # START MAXIMIZED OPTION
    START_MAXIMIZED = '--start-maximized'

    @property
    def _options(self):
        """
        chrome浏览器特有的操作属性
        :return:
        """
        if self.OPTION_MARK:
            chrome_option = self._option()
            chrome_option.headless = self.HEADLESS
            if self.WINDOW_SIZE:
                chrome_option.add_argument(self.WINDOW_SIZE)
            if self.START_MAXIMIZED:
                chrome_option.add_argument(self.START_MAXIMIZED)
            if  self.EXPERIMENTAL:
                for k, v in self.EXPERIMENTAL.items():
                    chrome_option.add_experimental_option(k, v)
            return chrome_option
        return None
    
    @property
    def browser(self):
        """
        启动chrome浏览器并进行初始配置
        :return:
        """
        if self._options:
            chrome = self._driver(self._path, options=self._options)
        else:
            chrome = self._driver(self._path)

        if self.METHOD_MARK:
            chrome.implicitly_wait(self.IMPLICITLY_WAIT_TIME)
            chrome.set_page_load_timeout(self.PAGE_LOAD_TIME)
            chrome.set_script_timeout(self.SCRIPT_TIMEOUT)
            return chrome
        return chrome




#with CHROME().browser as _chrome:
#    _chrome.get('http://www.baidu.com')
#    from time import sleep
#    sleep(3)
#
#
# with IE().browser as _ie:
#     _ie.get('http://www.baidu.com')
#     from time import sleep
#     sleep(3)

# print(CHROME.mro())
