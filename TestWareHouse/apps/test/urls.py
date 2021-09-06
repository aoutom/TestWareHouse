from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.conf.urls import url, include
from app import forms, views

from apps.test.views import TestView, ExamView, ExamPageView, ajax_load_points, ExamResultView, TestListView
urlpatterns = [
    path('', TestView.as_view(), name='test'),
    url(r"^exam/$", ExamView.as_view(), name="exam"),
    url(r"^exam/(?P<random_token>[a-zA-Z0-9]{10,20})/$", ExamPageView.as_view(), name="exampage"),
    url(r"^exam/(?P<random_token>[a-zA-Z0-9]{10,20})/result/$", ExamResultView.as_view(), name="examresult"),
    path("ajax/load_points/", ajax_load_points, name="ajax_load_points"),
    url(r"^test_list\?.*$", TestListView.as_view(), name="test_list"),
    path("test_list/",TestListView.as_view(), name="test_list"),
    #path("exam/a/", ExamView)
    ]