from BasePage.BasePage import Basepage
from selenium_tools.ini_tool import  IniObject
#from selenium import webdriver
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
#from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.common.action_chains import ActionChains
import selenium
import configparser

class souhu_Loginpage(Basepage):

    sohu_login= IniObject(file="data.ini").get_section("Sohu_Login")

    def input_user_name(self,user_name_info):
        user_name_data=self.sohu_login.split_data(self.sohu_login.get_option_data("user_name"))
        user_name_method=user_name_data[0]
        user_name_path=user_name_data[1]
        self.send_content(self.get_element(user_name_method,user_name_path),user_name_info)

    def input_password(self,password_info):
        password_data=self.sohu_login.split_data(self.sohu_login.get_option_data("password"))
        password_method=password_data[0]
        password_path=password_data[1]
        self.send_content(self.get_element(password_method,password_path),password_info)

    def click_submit(self):
        submit_data=self.sohu_login.split_data(self.sohu_login.get_option_data("submit"))
        submit_method=submit_data[0]
        submit_path=submit_data[1]
        self.mouse_click(self.get_element(submit_method,submit_path))


    def judge_error_information(self,error_type,error_info):
        error_data=self.sohu_login.split_data(self.sohu_login.get_option_data(error_type))
        error_method=error_data[0]
        error_path=error_data[1]       
        if self.get_element(error_method,error_path)==None:
            return False
        if self.get_text(self.get_element(error_method,error_path))==error_info:
            return True
        else:
            return False


    #def click_element(self,element):
    #    submit_method=self.cf.get('Loginpage',element).split('>')[0]
    #    submit_path=self.cf.get('Loginpage',element).split('>')[1]
    #    self.mouse_click(self.get_element(submit_method,submit_path))



    #def judge_error_url(self,url,title):
    #    current_url=self.get_url()

    #    current_title=self.get_title()

    #    if url in current_url and title in current_title:
    #        return True
    #    else:
    #        return False

