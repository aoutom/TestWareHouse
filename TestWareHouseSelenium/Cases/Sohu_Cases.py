from Page.Sohu_Page import souhu_Loginpage


class souhu_login_test(souhu_Loginpage):
    def login_error_test(self,username,password,error_type,error_info):
        print(username,password,error_type,error_info)
        self.input_user_name(username)
        self.input_password(password)
        self.click_submit()
        return self.judge_error_information(error_type,error_info)

    #def jump_url_test(self,el_name,url,title):
    #    self.click_element(el_name)
    #    self.jump_current_url()
    #    return self.judge_error_url(url,title) 

    


