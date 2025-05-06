from django.contrib import admin
from .models import User_Account

class User_Account_admin(admin.ModelAdmin):
    list_display = ['email','username']

admin.site.register(User_Account, User_Account_admin)
