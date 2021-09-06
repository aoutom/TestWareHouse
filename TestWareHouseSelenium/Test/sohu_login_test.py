from Cases.Sohu_Cases import souhu_login_test
from selenium_tools.excel_tool import ExcelObject
from selenium_tools.browser import CHROME
from selenium_tools.log_tool import CreateLog
from selenium_tools.html_runner_tool import html_runner
#from selenium import webdriver
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
#from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.common.action_chains import ActionChains
import selenium
import unittest
import time
import os
import ddt
#from log.use_log import CreateLog
import sys
import HTMLTestRunner
ex=ExcelObject(file="souhu_login.xlsx")
ex_data=ex.read("login")
@ddt.ddt
class FirstDdtCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.user=CreateLog()
        self.logger=self.user.get_log()
    @classmethod
    def tearDownClass(self):
        self.user.close_log()

    def setUp(self):

        self.driver = CHROME().browser
        self.driver.get("https://v4.passport.sohu.com/fe/login")
        self.login = souhu_login_test(self.driver)

    def tearDown(self):
        time.sleep(2)
        false_ty=False
        for method_name,error in self._outcome.errors:
              if error:
                  false_ty=True
                  case_name = self._testMethodName
                  file_path = os.path.join("C:/Users/86187/source/repos/selenium_PO/selenium_PO/"+"report/"+case_name+".png")
                  self.driver.save_screenshot(file_path)
        if false_ty:
            self.logger.info("测试用例执行失败")
        else:
            self.logger.info("测试用例执行成功")
        self.driver.close()
        
     
    @ddt.data(*ex_data)
    def test_login_case(self,data):
        username,password,error_type,error_info=data
        result=self.login.login_error_test(username,password,error_type,error_info)

        return self.assertTrue(result)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(FirstDdtCase)
    #suite1=unittest.TestSuite()
    #suite1.addTest(FirstDdtCase('test_register_case_1'))
    #suite1.addTest(FirstDdtCase('test_jump_case_2'))
    result=html_runner(suite,add_name="souhu_login_test",title="souhu_login_test",description=u"souhu登录页面测试")
    print(result)
    #unittest.main






