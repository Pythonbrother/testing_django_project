from django.contrib import admin
from .models import User_Account

class User_Account_admin(admin.ModelAdmin):
    list_display = ['email','username','last_login', 'is_active']

admin.site.register(User_Account, User_Account_admin)

admin.site.site_header = "Diagnosis System"
admin.site.site_title = "Adminstration Site"