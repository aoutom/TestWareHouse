from django.core.mail import send_mail, EmailMultiAlternatives
from TestWareHouse.settings import EMAIL_FROM
from django.template import Context, loader

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

#def send_forget_password_code(email,code):
#    email_title="TestWareHouse邮箱验证码"
    
#    email_boby="本链接一小时内有效，请点击链接验证：<h1><a href='http://127.0.0.1:8000/testhouse/forget_password/{}'>Click</a></h1>".format(code)
#    k=send_mail(email_title, email_boby, EMAIL_FROM, [email])
#    n=0
#    while not k and n<3:
#        k=send_mail(email_title, email_boby, EMAIL_FROM, [email], )
#        n+=1
#    if k:
#        return True
#    else:
#        return False
def send_forget_password_code(email,code):
    email_title="TestWareHouse邮箱验证码"
    
    email_boby="本链接一小时内有效，请点击链接验证：<h1><a href='http://127.0.0.1:8000/testhouse/forget_password/{}'>Click</a></h1>".format(code)
    html="<h1>本链接一小时内有效，请点击链接验证：</h1><h2><a href='http://127.0.0.1:8000/testhouse/forget_password/{}'>Click</a></h2>".format(code)
    mail=EmailMultiAlternatives(email_title, email_boby, EMAIL_FROM, [email])
    mail.attach_alternative(html,"text/html")
    #msg.attach_file(u'D:/My Documents/Python/doc/test.doc')        # 添加附件发送
    
    n=0
    while n<3:
        try:
            mail.send()
        except:
            n+=1
        else:
            return True
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
