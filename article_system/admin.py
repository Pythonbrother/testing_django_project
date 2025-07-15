from django.contrib import admin
from .models import *

class Article_Admin(admin.ModelAdmin):
    list_display = ['id', 'name', 'creator', 'created_time']

class CommentArticle_Admin(admin.ModelAdmin):
    list_display = ['pk', 'commenter']

class CommentComment_Admin(admin.ModelAdmin):
    list_display = ['pk', 'commenter']

admin.site.register(Article, Article_Admin)
admin.site.register(Comment_to_Article, CommentArticle_Admin)
admin.site.register(Comment_to_Comment, CommentComment_Admin)