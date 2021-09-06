"""
Definition of urls for TestWareHouse.
"""
from django.conf import settings


from datetime import datetime
from django.urls import path,re_path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.views.static import  serve
from django.conf.urls import url,include
from apps.users.views import IndexView
from apps.test.views import TestView, ExamView, ExamPageView, ajax_load_points
urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),


    path('admin/', admin.site.urls),
    path("testhouse/",include('apps.users.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^ueditor/',include('DjangoUeditor.urls' )),
    path("testhouse/test/", include("apps.test.urls")),
    #path('test/logout/', LogoutView.as_view(), name='logout'),
    path("ajax/load_points/", ajax_load_points, name="ajax_load_points"),
    path("testhouse/user_home/", include("apps.operation.urls")),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
]
