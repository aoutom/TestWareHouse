from django.contrib import admin
from apps.test.models import TestSubject, Test, TestPoint

class TestSubjectAdmin(admin.ModelAdmin):
    list_display=["subject"]
    search_fields=["subject"]
    list_filter=["subject"] 

class TestPointAdmin(admin.ModelAdmin):
    list_display=["subject","point"]
    search_fields=["subject","point"]
    list_filter=["subject"] 

class TestAdmin(admin.ModelAdmin):
    list_display=["status","subject_point","style","difficulty","desc","all_nums","correct_nums","collection_nums","threshold"]
    search_fields=["status","subject_point","style","difficulty","all_nums","correct_nums","collection_nums"]
    list_filter=["subject_point","style","difficulty","status",] 


admin.site.register(TestSubject, TestSubjectAdmin)
admin.site.register(TestPoint, TestPointAdmin)
admin.site.register(Test, TestAdmin)
# Register your models here.
