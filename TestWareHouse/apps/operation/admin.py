from django.contrib import admin
from apps.operation.models import UserTest, UserFavourite, UserSubmit, TestVerify, TestObjection, TestMessage

class UserTestAdmin(admin.ModelAdmin):
    list_display=["user","test","is_true","is_false","is_active"]
    search_fields=["user","test","is_true","is_false","is_active"]
    list_filter=["user","test","is_true","is_false","is_active"] 

class UserFavouriteAdmin(admin.ModelAdmin):
    list_display=["user","test","is_active"]
    search_fields=["user","test","is_active"]
    list_filter=["user","test","is_active"] 
    #list_editable=["mobile"]
# Register your models here.

class UserSubmitAdmin(admin.ModelAdmin):
    list_display=["user","test","is_active"]
    search_fields=["user","test","is_active"]
    list_filter=["user","test","is_active"] 

class TestVerifyAdmin(admin.ModelAdmin):
    list_display=["user","test","is_verify"]
    search_fields=["user","test","is_verify"]
    list_filter=["user","test","is_verify"] 


class TestObjectionAdmin(admin.ModelAdmin):
    list_display=["user","test","is_active"]
    search_fields=["user","test","is_active"]
    list_filter=["user","test","is_active"] 

class TestMessageAdmin(admin.ModelAdmin):
    list_display=["user","test","is_active"]
    search_fields=["user","test","is_active"]
    list_filter=["user","test","is_active"] 
admin.site.register(UserTest, UserTestAdmin)
admin.site.register(UserFavourite, UserFavouriteAdmin)
admin.site.register(UserSubmit, UserSubmitAdmin)
admin.site.register(TestVerify, TestVerifyAdmin)
admin.site.register(TestObjection, TestObjectionAdmin)
admin.site.register(TestMessage, TestMessageAdmin)
# Register your models here.
