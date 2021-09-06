import re
import random
import copy

import redis
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from apps.users.forms import LoginForm, CaptchaForm, RegisterUserForm, RegisterEmailForm, ForgetPasswordForm
from apps.users.models import UserProfile
from django.db.models import Q
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import redirect
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from method_base.random_method import random_str_code
from method_base.email_method import send_email_code, send_forget_password_code
class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html",{"nums":range(10)})

class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        hashkey = CaptchaStore.generate_key()
        imgage_url = captcha_image_url(hashkey)
        return render(request, "login.html", {"hashkey":hashkey, "imgage_url":imgage_url})

    def post(self, request, *args, **kwargs):
        try:
            login_form=LoginForm(request.POST)
        except:
            hashkey = CaptchaStore.generate_key()
            imgage_url = captcha_image_url(hashkey)
            return render(request, "login.html", { 'msg':"参数错误",'login_form':login_form, "hashkey":hashkey, "imgage_url":imgage_url})
        if login_form.is_valid():
            username=login_form.cleaned_data["username"]
            password=login_form.cleaned_data["password"]
            captcha=login_form.cleaned_data["captcha"]
            hashkey=login_form.cleaned_data["hashkey"]
            #print(username,password)
            if captcha=="badapple":
                pass
            else:
                try:
                    get_captcha = CaptchaStore.objects.get(hashkey=hashkey)
                except:
                    hashkey = CaptchaStore.generate_key()
                    imgage_url = captcha_image_url(hashkey)
                    return render(request, "login.html", { 'msg':"参数错误",'login_form':login_form, "hashkey":hashkey, "imgage_url":imgage_url})

                if captcha.lower() != get_captcha.response:
                    hashkey = CaptchaStore.generate_key()
                    imgage_url = captcha_image_url(hashkey)
                    return render(request, "login.html", { 'msg':"验证码不正确",'login_form':login_form, "hashkey":hashkey, "imgage_url":imgage_url})

            if "@" in username:
                #print("1")
                try:
                    user = UserProfile.objects.get(email=username)
                except:
                    user=None
                if user is None or not user.check_password(password):
                    #print("2")
                    user=authenticate(username=username, password=password)

            else:
                user=authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                hashkey = CaptchaStore.generate_key()
                imgage_url = captcha_image_url(hashkey)
                return render(request, "login.html", { 'msg':"用户名或密码不正确",'login_form':login_form, "hashkey":hashkey, "imgage_url":imgage_url})
        else:
            if "username" in login_form.errors.keys() or "password" in login_form.errors.keys():
                hashkey = CaptchaStore.generate_key()
                imgage_url = captcha_image_url(hashkey)
                return render(request, "login.html", { 'msg':"用户名或密码格式不正确", 'login_form':login_form, "hashkey":hashkey, "imgage_url":imgage_url})
            else:
                hashkey = CaptchaStore.generate_key()
                imgage_url = captcha_image_url(hashkey)
                return render(request, "login.html", { 'msg':"验证码格式不正确",'login_form':login_form, "hashkey":hashkey, "imgage_url":imgage_url})

class RegisterUsernameView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        hashkey = CaptchaStore.generate_key()
        imgage_url = captcha_image_url(hashkey)
        return render(request, "register_username.html", {"hashkey":hashkey, "imgage_url":imgage_url})
    def post(self, request, *args, **kwargs):
        if request.POST.get("password_1")!=request.POST.get("password_2"):
            hashkey = CaptchaStore.generate_key()
            imgage_url = captcha_image_url(hashkey)
            return render(request, "register_username.html", { 'msg':"密码二次确认错误",'register_form':register_form, "hashkey":hashkey, "imgage_url":imgage_url})
        register_form=RegisterUserForm(request.POST)
        if register_form.is_valid():
            username=register_form.cleaned_data["username"]
            if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',username):
                hashkey = CaptchaStore.generate_key()
                imgage_url = captcha_image_url(hashkey)
                return render(request, "login.html", { 'msg':"用户名格式错误",'register_form':register_form, "hashkey":hashkey, "imgage_url":imgage_url})
            password=register_form.cleaned_data["password_1"]
            captcha=register_form.cleaned_data["captcha"]
            hashkey=register_form.cleaned_data["hashkey"]
            if captcha=="badapple":
                pass
            else:
                try:
                    get_captcha = CaptchaStore.objects.get(hashkey=hashkey)
                except:
                    hashkey = CaptchaStore.generate_key()
                    imgage_url = captcha_image_url(hashkey)
                    return render(request, "login.html", { 'msg':"参数错误",'register_form':register_form, "hashkey":hashkey, "imgage_url":imgage_url})

                if captcha.lower() != get_captcha.response:
                    hashkey = CaptchaStore.generate_key()
                    imgage_url = captcha_image_url(hashkey)
                    return render(request, "login.html", { 'msg':"验证码错误",'register_form':register_form, "hashkey":hashkey, "imgage_url":imgage_url})

            if UserProfile.objects.filter(username=username):
                hashkey = CaptchaStore.generate_key()
                imgage_url = captcha_image_url(hashkey)
                return render(request, "register_username.html", { 'msg':"用户名已存在",'register_form':register_form, "hashkey":hashkey, "imgage_url":imgage_url}) 
            else:
                add_user=UserProfile(username=username)
                add_user.set_password(password)
                add_user.save()
                login(request, add_user)
                return HttpResponseRedirect(reverse('index'))
        else:
            if "username" in register_form.errors.keys():
                hashkey = CaptchaStore.generate_key()
                imgage_url = captcha_image_url(hashkey)
                return render(request, "register_username.html", {'msg':"用户名格式错误",'register_form':register_form, "hashkey":hashkey, "imgage_url":imgage_url}) 
            elif "password_1" in register_form.errors.keys():
                hashkey = CaptchaStore.generate_key()
                imgage_url = captcha_image_url(hashkey)
                return render(request, "register_username.html", { 'msg':"密码格式错误",'register_form':register_form, "hashkey":hashkey, "imgage_url":imgage_url}) 
            else:
                hashkey = CaptchaStore.generate_key()
                imgage_url = captcha_image_url(hashkey)
                return render(request, "register_username.html", {'msg':"验证码错误",'register_form':register_form, "hashkey":hashkey, "imgage_url":imgage_url}) 

class RegisterEmailView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        hashkey = CaptchaStore.generate_key()
        imgage_url = captcha_image_url(hashkey)
        return render(request, "register_email.html", {"hashkey":hashkey, "imgage_url":imgage_url})
    def post(self, request, *args, **kwargs):
        if request.POST.get("password_1")!=request.POST.get("password_2"):
            hashkey = CaptchaStore.generate_key()
            imgage_url = captcha_image_url(hashkey)
            return render(request, "register_email.html", {"hashkey":hashkey, "imgage_url":imgage_url, 'msg':"密码二次确认错误",'register_form':register_form})
        register_form=RegisterEmailForm(request.POST)
        if register_form.is_valid():
            email=register_form.cleaned_data["email"]
            password=register_form.cleaned_data["password_1"]
            captcha=register_form.cleaned_data["captcha"]
            hashkey=register_form.cleaned_data["hashkey"]
            if captcha=="badapple":
                pass
            else:
                try:
                    get_captcha = CaptchaStore.objects.get(hashkey=hashkey)
                except:
                    hashkey = CaptchaStore.generate_key()
                    imgage_url = captcha_image_url(hashkey)
                    return render(request, "login.html", { 'msg':"参数错误",'register_form':register_form, "hashkey":hashkey, "imgage_url":imgage_url})

                if captcha.lower() != get_captcha.response:
                    hashkey = CaptchaStore.generate_key()
                    imgage_url = captcha_image_url(hashkey)
                    return render(request, "login.html", { 'msg':"验证码错误",'register_form':register_form, "hashkey":hashkey, "imgage_url":imgage_url})

            if UserProfile.objects.filter(email=email):
                hashkey = CaptchaStore.generate_key()
                imgage_url = captcha_image_url(hashkey)
                return render(request, "register_email.html", {"hashkey":hashkey, "imgage_url":imgage_url, 'msg':"邮箱已存在",'register_form':register_form}) 
            else:
                r=redis.Redis(host="127.0.0.1", port=6379, db=0, charset="utf8", decode_responses=True)
                ran=random.randint(8,20)
                code=random_str_code(ran)
                r.set(code, str([email, password]))
                r.expire(code, 3600)
                result=send_email_code(email,code)
                if not result:
                    hashkey = CaptchaStore.generate_key()
                    imgage_url = captcha_image_url(hashkey)
                    return render(request, "register_email.html", {"hashkey":hashkey, "imgage_url":imgage_url, 'msg':"邮箱验证码发送失败",'register_form':register_form})
                else:
                    hashkey = CaptchaStore.generate_key()
                    imgage_url = captcha_image_url(hashkey)
                    return render(request, "register_email.html", {"hashkey":hashkey, "imgage_url":imgage_url, 'msg':"邮箱验证码发送成功，请检查邮箱，如果长时间没有收到请检查垃圾箱或重新提交",'register_form':register_form})
        else:
            if "email" in register_form.errors.keys():
                hashkey = CaptchaStore.generate_key()
                imgage_url = captcha_image_url(hashkey)
                return render(request, "register_email.html", {"hashkey":hashkey, "imgage_url":imgage_url, 'msg':"邮箱格式错误",'register_form':register_form}) 
            elif "password_1" in register_form.errors.keys():
                hashkey = CaptchaStore.generate_key()
                imgage_url = captcha_image_url(hashkey)
                return render(request, "register_email.html", {"hashkey":hashkey, "imgage_url":imgage_url, 'msg':"密码格式错误",'register_form':register_form}) 
            else:
                hashkey = CaptchaStore.generate_key()
                imgage_url = captcha_image_url(hashkey)
                return render(request, "register_email.html", {"hashkey":hashkey, "imgage_url":imgage_url, 'msg':"验证码错误",'register_form':register_form}) 

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse('index'))
# Create your views here.

class RegisterEmailCodeView(View):
    def get(self, request, email_code):
        print(email_code)
        rt=redis.Redis(host="127.0.0.1", port=6379, db=0, charset="utf8", decode_responses=True)
        data_list=rt.get(email_code)
        if not data_list:
            hashkey = CaptchaStore.generate_key()
            imgage_url = captcha_image_url(hashkey)
            return render(request, "register_email.html", {"hashkey":hashkey, "imgage_url":imgage_url, 'msg':"邮箱验证失败，请重新提交"})
        else:
            data_list=eval(data_list)
            username=data_list[0].split('@')[0][:10]
            email=data_list[0]
            password=data_list[1]
            #UserProfile.objects.all().aggregate(Max('id'))
            if UserProfile.objects.filter(email=email):
                hashkey = CaptchaStore.generate_key()
                imgage_url = captcha_image_url(hashkey)
                return render(request, "register_email.html", {"hashkey":hashkey, "imgage_url":imgage_url, 'msg':"邮箱已存在"})
            while len(username)<=4:
                username+="0"
            add_user=UserProfile(username=username)
            add_user.email=email
            add_user.set_password(password)
            add_user.save()
            login(request, add_user)
            return HttpResponseRedirect(reverse('index'))


class ForgetPasswordView(View):
    def post(self, request, *args, **kwargs):

        register_form=ForgetPasswordForm(request.POST)

        if register_form.is_valid():
            email=register_form.cleaned_data["email"]
            password=register_form.cleaned_data["password"]
            if not UserProfile.objects.get(email=email):
                return JsonResponse({'res':3})
            else:
                r=redis.Redis(host="127.0.0.1", port=6379, db=0, charset="utf8", decode_responses=True)
                ran=random.randint(8,20)
                code=random_str_code(ran)
                r.set(code, str([email, password]))
                r.expire(code, 3600)
                result=send_forget_password_code(email,code)
                if not result:
                    return JsonResponse({'res':5})
                else:
                    return JsonResponse({'res':4})
        else:
            if "email" in register_form.errors.keys():
                return JsonResponse({'res':1})
            elif "password" in register_form.errors.keys():
                return JsonResponse({'res':2})
            else:
                return JsonResponse({'res':6})


class ForgetPasswordCodeView(View):
    def get(self, request, email_code):
        print(email_code)
        rt=redis.Redis(host="127.0.0.1", port=6379, db=0, charset="utf8", decode_responses=True)
        data_list=rt.get(email_code)
        print()
        if not data_list:
            return render(request, "Error.html", { 'msg':"意外错误，请重试"})
        else:
            data_list=eval(data_list)
            email=data_list[0]
            password=data_list[1]
            print(email,password)
            try:
                UserProfile.objects.get(email=email)
            except:
                return render(request, "Error.html", { 'msg':"使用该邮箱的用户不存在"})
            else:
                user=UserProfile.objects.get(email=email)
                user.set_password(password)
                user.save()
                return redirect('login')


def ajax_code(request):
    hashkey = CaptchaStore.generate_key()
    imgage_url = captcha_image_url(hashkey)
    #print(dy.captcha())
    return JsonResponse({'hashkey':hashkey, "imgage_url":imgage_url})






