from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.conf.urls import url, include
#from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

from apps.users.views import IndexView, LoginView, RegisterUsernameView, LogoutView, RegisterEmailView, RegisterEmailCodeView, ForgetPasswordView, ForgetPasswordCodeView , ajax_code
from apps.test.views import TestView
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('register_username/', RegisterUsernameView.as_view(), name='register_username'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register_email/', RegisterEmailView.as_view(), name='register_email'),
    url(r"^register_email_code/(?P<email_code>.*)/$", RegisterEmailCodeView.as_view(), name='register_email_code'),
    path("test/", include("apps.test.urls")),
    path("forget_password/", ForgetPasswordView.as_view(), name="forget_password"),
    url(r"^forget_password/(?P<email_code>.*)/$", ForgetPasswordCodeView.as_view(), name="forget_passwoed_code"),
    path("ajax_code/", ajax_code, name="ajax_code"),
    ]
