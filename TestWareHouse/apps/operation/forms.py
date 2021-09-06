from django import forms
from captcha.fields import CaptchaField
from django.core.validators import RegexValidator


class ChangePasswordForm(forms.Form):
    password=forms.CharField(required=True, min_length=6, max_length=20, validators=[RegexValidator(r"(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}","格式不正确")])
    password_1=forms.CharField(required=True, min_length=6, max_length=20, validators=[RegexValidator(r"(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}","格式不正确")])
    password_2=forms.CharField(required=True, min_length=6, max_length=20, validators=[RegexValidator(r"(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}","格式不正确")])

class ChangeEmailForm(forms.Form):
    email=forms.CharField(required=True,  validators=[RegexValidator(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',"格式不正确")])