from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import selenium
import time
class Basepage():
    def __init__(self, driver):
        self.dr=driver
    def get_element(self,method,path, wait_time=10):
        if method=="xpath":
            loc=(By.XPATH,path)
            try:
                WebDriverWait(self.dr,wait_time).until(EC.visibility_of_element_located(loc))
            except TimeoutException:
                return None
            else:
                return self.dr.find_element_by_xpath(path)

        elif method=="id":
            loc=(By.ID,path)
            try:
                WebDriverWait(self.dr,wait_time).until(EC.visibility_of_element_located(loc))
            except TimeoutException:
                return None
            else:
                return self.dr.find_element_by_id(path)



    def send_content(self,element,content):
        element.send_keys(content)

    def mouse_click(self,info):
        if type(info)==list:
            ActionChains(self.dr).move_by_offset(info[0],info[1]).click().perform()
        elif type(info)==selenium.webdriver.remote.webelement.WebElement:
            ActionChains(self.dr).move_to_element(info).click().perform()

    def get_text(self,element):
        return element.text

    def get_url(self):
        return self.dr.current_url

    def get_title(self):
        return self.dr.title

    def jump_current_url(self):
        time.sleep(1)
        if len(self.dr.window_handles)==1:
            self.dr.switch_to.window(self.dr.window_handles[0])
        else:
            self.dr.switch_to.window(self.dr.window_handles[1])

    def get_elements(self,method,path, wait_time=10):
        if method=="xpath":
            loc=(By.XPATH,path)
            try:
                WebDriverWait(self.dr,wait_time).until(EC.visibility_of_element_located(loc))
            except TimeoutException:
                return None
            else:
                return self.dr.find_elements_by_xpath(path)