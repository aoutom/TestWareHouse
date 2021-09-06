from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.conf.urls import url, include
from app import forms, views

from apps.operation.views import UserHomeView, ChangeUserNameView, ChangePasswordView, ChangeEmailView, ChangeEmailCodeView, WrongTestListView, AjaxWrongTestView, FavouriteTestListView, AjaxFavouriteTestView, AjaxHabitView, AjaxChangePageView, UserTestSubmitView, AjaxChangeSubjectView, StaffVerifyView, SubmitTestListView, AjaxSubmitTestView, StaffTestDetailView, AjaxVerifyDelete, AjaxVerifyUse
urlpatterns = [
    path('', UserHomeView.as_view(), name='userhome'),
    path('changeusername/', ChangeUserNameView.as_view(), name='changeusername'),
    path('changepassword/', ChangePasswordView.as_view(), name='changepassword'),
    path('changeemail/', ChangeEmailView.as_view(), name='changeemail'),
    url(r"^change_email_code/(?P<email_code>.*)/$", ChangeEmailCodeView.as_view(), name='change_email_code'),
    path("wrong_test_list/", WrongTestListView.as_view(), name="wrongtestlist"),
    path("ajax_wrong_test/", AjaxWrongTestView.as_view(), name="ajaxwrongtest"),
    path("ajax_favourite_test/", AjaxFavouriteTestView.as_view(), name="ajaxfavouritetest"),
    path("favourite_test_list/", FavouriteTestListView.as_view(), name="favouritetestlist"),
    path('ajax_habit/', AjaxHabitView.as_view(), name='ajaxhabit'),
    path('ajax_change_page/', AjaxChangePageView.as_view(),name="ajaxchangepage"),
    path('user_test_submit/', UserTestSubmitView.as_view(),name="usertestsubmit"),
    path('ajax_change_subject/', AjaxChangeSubjectView.as_view(),name="ajaxchangesubject"),
    path("staff_home_page/", StaffVerifyView.as_view(), name="staffhomepage"),
    path("submit_test_list/", SubmitTestListView.as_view(), name="submittestlist"),
    path("ajax_submit_test/", AjaxSubmitTestView.as_view(), name="ajaxsubmittest"),
    path("staff_home_page/staff_test_detail/", StaffTestDetailView.as_view(), name="stafftestdetail"),
    path("ajax_verify_delete/", AjaxVerifyDelete.as_view(), name="ajaxverifydelete"),
    path("ajax_verify_use/", AjaxVerifyUse.as_view(), name="ajaxverifyuse"),
    ]