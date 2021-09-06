from django import forms
from captcha.fields import CaptchaField
from django.core.validators import RegexValidator
import re

class CaptchaForm(forms.Form):
    captcha=CaptchaField()

class LoginForm(forms.Form):
    username=forms.CharField(required=True, validators=[RegexValidator(r"^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$|.{1,20}","格式不正确")])
    password=forms.CharField(required=True, min_length=6, max_length=20, validators=[RegexValidator(r"(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}","格式不正确")])
    captcha=forms.CharField(required=True, min_length=4, max_length=10)
    hashkey=forms.CharField(required=True)
class RegisterUserForm(forms.Form):
    username=forms.CharField(required=True, min_length=1, max_length=20)
    password_1=forms.CharField(required=True, min_length=6, max_length=20, validators=[RegexValidator(r"(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}","格式不正确")])
    password_2=forms.CharField(required=True, min_length=6, max_length=20, validators=[RegexValidator(r"(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}","格式不正确")])
    captcha=forms.CharField(required=True, min_length=4, max_length=10)
    hashkey=forms.CharField(required=True)

    def clean_username(self):
        username=self.cleaned_data["username"]
        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',username):
            raise forms.ValidationError("用户名格式错误")
        else:
            return username

class RegisterEmailForm(forms.Form):
    email=forms.CharField(required=True,  validators=[RegexValidator(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',"格式不正确")])
    password_1=forms.CharField(required=True, min_length=6, max_length=20, validators=[RegexValidator(r"(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}","格式不正确")])
    password_2=forms.CharField(required=True, min_length=6, max_length=20, validators=[RegexValidator(r"(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}","格式不正确")])
    captcha=forms.CharField(required=True, min_length=4, max_length=10)
    hashkey=forms.CharField(required=True)

class ForgetPasswordForm(forms.Form):
    email=forms.CharField(required=True,  validators=[RegexValidator(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',"格式不正确")])
    password=forms.CharField(required=True, min_length=6, max_length=20, validators=[RegexValidator(r"(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{6,20}","格式不正确")])