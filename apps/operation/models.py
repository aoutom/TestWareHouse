from django.db import models

from apps.users.models import BaseModel, UserProfile
from apps.test.models import Test

class UserTest(BaseModel):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    test=models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="题目")
    is_true=models.IntegerField( verbose_name="是否对过", default=0)
    is_false=models.IntegerField( verbose_name="是否错过", default=0)
    is_active=models.IntegerField(verbose_name="是否启用", default=1)

    class Meta:
        verbose_name="做题记录"
        verbose_name_plural = verbose_name
        unique_together=(("user","test"),)

    def __str__(self):
        return self.user.username+"_"+self.test.desc

class UserFavourite(BaseModel):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    test=models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="题目")
    is_active=models.IntegerField(verbose_name="是否启用", default=1)

    class Meta:
        verbose_name="收藏记录"
        verbose_name_plural = verbose_name
        unique_together=(("user","test"),)

    def __str__(self):
        return self.user.username+"_"+self.test.desc

class UserSubmit(BaseModel):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    test=models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="题目")
    is_active=models.IntegerField(verbose_name="是否启用", default=1)

    class Meta:
        verbose_name="提交试题记录"
        verbose_name_plural = verbose_name
        unique_together=(("user","test"),)

    def __str__(self):
        return self.user.username+"_"+self.test.desc

class TestVerify(BaseModel):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="审核员")
    test=models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="题目")
    is_verify=models.IntegerField(verbose_name="是否审核", default=0)

    class Meta:
        verbose_name="试题审核记录"
        verbose_name_plural = verbose_name
        unique_together=(("user","test"),)

    def __str__(self):
        return self.user.username+"_"+self.test.desc

class TestObjection(BaseModel):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    test=models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="题目")
    content=models.TextField(verbose_name="异议内容")
    is_active=models.IntegerField(verbose_name="是否有效", default=0)

    class Meta:
        verbose_name="试题异议"
        verbose_name_plural = verbose_name
        unique_together=(("user","test"),)

    def __str__(self):
        return self.user.username+"_"+self.test.desc


class TestMessage(BaseModel):
    user=models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    test=models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="题目")
    content=models.TextField(verbose_name="评论内容")
    is_active=models.IntegerField(verbose_name="是否有效", default=0)

    class Meta:
        verbose_name="试题评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username+"_"+self.test.desc