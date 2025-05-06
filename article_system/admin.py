from django.contrib import admin
from .models import *

class Article_Admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'creator', 'created_time']

admin.site.register(Article, Article_Admin)