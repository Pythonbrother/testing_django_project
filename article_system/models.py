from django.db import models
from account_system.models import User_Account

class Article(models.Model):
    name = models.CharField(max_length=30)
    caption = models.TextField(null=True, blank=True)
    topic = models.TextField()
    photo = models.ImageField(upload_to='article_photos/', null=True, blank=True)
    creator = models.ForeignKey(User_Account, on_delete=models.SET_NULL, null=True, blank=True, default="unknown")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

class Comment_to_Article(models.Model):
    comment = models.TextField(null=True,blank=True)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, blank=True)
    commenter = models.ForeignKey(User_Account, on_delete=models.SET_NULL, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

class Comment_to_Comment(models.Model):
    comment = models.TextField(null=True, blank=True)
    target_comment = models.ForeignKey(Comment_to_Article, on_delete=models.SET_NULL, null=True, blank=True)
    commenter = models.ForeignKey(User_Account, on_delete=models.SET_NULL, null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

