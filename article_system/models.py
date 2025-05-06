from django.db import models
from account_system.models import User_Account

class Article(models.Model):
    name = models.CharField(max_length=30)
    topic_type = models.CharField(choices=[('Disease','Disease'),('Tools','Tools'),('Medicine','Medicine'),('Behaviour','Behaviour')], max_length=20)
    caption = models.TextField(null=True, blank=True)
    topic = models.TextField()
    symptoms = models.TextField(null=True, blank=True)
    causes = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='article_photos/', null=True, blank=True)
    creator = models.ForeignKey(User_Account, on_delete=models.SET_NULL, null=True, blank=True, default="unknown")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


