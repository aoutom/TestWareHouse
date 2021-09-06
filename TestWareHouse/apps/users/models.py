from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        abstract = True

class UserProfile(AbstractUser):

    image = models.ImageField(verbose_name="用户头像", upload_to="head_image/%Y/%m", default="default.jpg")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    habit=models.IntegerField(default=1, verbose_name="看题习惯", choices=((1,"做题模式"),(2,"背题模式")))
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
