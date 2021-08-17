from django.core.mail import send_mail
from TestWareHouse.settings import EMAIL_FROM
def send_email_code(email,code):
    email_title="TestWareHouse邮箱验证码"
    email_boby="本链接一小时内有效，请点击链接验证：<h1><a href='http://127.0.0.1:8000/testhouse/register_email_code/{}'>Click</a></h1>".format(code)
    k=send_mail(email_title, email_boby, EMAIL_FROM, [email], )
    n=0
    while not k and n<3:
        k=send_mail(email_title, email_boby, EMAIL_FROM, [email], )
        n+=1
    if k:
        return True
    else:
        return False

def send_forget_password_code(email,code):
    email_title="TestWareHouse邮箱验证码"
    
    email_boby="本链接一小时内有效，请点击链接验证：<h1><a href='http://127.0.0.1:8000/testhouse/forget_password/{}'>Click</a></h1>".format(code)
    k=send_mail(email_title, email_boby, EMAIL_FROM, [email], html_message=True)
    n=0
    while not k and n<3:
        k=send_mail(email_title, email_boby, EMAIL_FROM, [email], )
        n+=1
    if k:
        return True
    else:
        return False

def send_change_email_code(email,code):
    email_title="TestWareHouse邮箱验证码"
    email_boby="本链接一小时内有效，请点击链接验证：<h1><a href='http://127.0.0.1:8000/testhouse/user_home/change_email_code/{}'>Click</a></h1>".format(code)
    k=send_mail(email_title, email_boby, EMAIL_FROM, [email], )
    n=0
    while not k and n<3:
        k=send_mail(email_title, email_boby, EMAIL_FROM, [email], )
        n+=1
    if k:
        return True
    else:
        return False
