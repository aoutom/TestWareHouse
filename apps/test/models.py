from django.db import models
#from DjangoUeditor.models import UEditorField
from ckeditor_uploader.fields import RichTextUploadingField
from apps.users.models import BaseModel
# Create your models here.
SUBJECT_CHOICE=(
    ("1","计算机网络"),
    ("2","计算机操作系统"),
    ("3","python基础"),
    ("4","java基础"),
    )





class TestSubject(BaseModel):
    subject=models.CharField(max_length=20, verbose_name="知识方向")
    class Meta:
        verbose_name = "知识方向"
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.subject

class TestPoint(BaseModel):
    subject=models.ForeignKey(TestSubject, on_delete=models.CASCADE, verbose_name="知识方向")
    point=models.CharField(max_length=20, verbose_name="知识点")

    class Meta:
        verbose_name = "知识点"
        verbose_name_plural = verbose_name
        unique_together=(("subject","point"),)

    def __str__(self):
        return self.subject.subject+"_"+self.point

class Test(BaseModel):
    subject_point=models.ForeignKey(TestPoint, on_delete=models.CASCADE, verbose_name="试题知识点")
    difficulty=models.CharField(max_length=1, choices=(("1","简单"),("2","中等"),("3","困难")), verbose_name="试题难度")
    style=models.CharField(max_length=1, choices=(("1","单选"),("2","多选"),("3","判断"),("4","填空")), verbose_name="试题类型")
    desc=models.TextField(verbose_name="试题描述")
    answer=models.CharField(max_length=200, verbose_name="试题答案")
    explain=RichTextUploadingField(verbose_name="试题解答",default="暂无")
    all_nums=models.IntegerField(default=1, verbose_name="被做次数")
    correct_nums=models.IntegerField(default=1, verbose_name="做对次数")
    collection_nums=models.IntegerField(default=0, verbose_name="收藏次数")
    status=models.CharField(max_length=1, choices=(("1","待审核"),("2","异议退回"),("3","启用"),("4","仅自己可见"),("5","废弃")), verbose_name="试题状态",default="1")
    threshold=models.IntegerField(default=5, verbose_name="异议阈值")
    objection_nums=models.IntegerField(default=0, verbose_name="异议次数")
    select_nums=models.IntegerField(default=0, verbose_name="选项个数")
    select_a=models.CharField(max_length=50, verbose_name="选项a",default="未知", blank=True)
    select_b=models.CharField(max_length=50, verbose_name="选项b",default="未知", blank=True)
    select_c=models.CharField(max_length=50, verbose_name="选项c",default="未知", blank=True)
    select_d=models.CharField(max_length=50, verbose_name="选项d",default="未知", blank=True)
    select_e=models.CharField(max_length=50, verbose_name="选项e",default="未知", blank=True)
    select_f=models.CharField(max_length=50, verbose_name="选项f",default="未知", blank=True)
    select_g=models.CharField(max_length=50, verbose_name="选项g",default="未知", blank=True)
    select_h=models.CharField(max_length=50, verbose_name="选项h",default="未知", blank=True)

    class Meta:
        verbose_name = "试题集"
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.desc
