from django.contrib import admin
from apps.users.models import UserProfile
class UsersAdmin(admin.ModelAdmin):
    list_display=["id","username","add_time",'habit']
    search_fields=["id","username","add_time",'habit']
    list_filter=["add_time"] 

    #list_editable=["mobile"]
# Register your models here.

admin.site.register(UserProfile, UsersAdmin)