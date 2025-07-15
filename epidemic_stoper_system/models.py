from django.db import models
from account_system.models import User_Account

class Epidemic(models.Model):
    name = models.CharField(max_length=30)
    topic = models.TextField(null=True, blank=True)
    symptoms = models.TextField()
    food_avoid = models.TextField(null=True, blank=True)  # for protection
    food_take = models.TextField(null=True, blank=True)  # for protection
    lifestyle_avoid = models.TextField(null=True, blank=True)  # for protection
    lifestyle_take = models.TextField(null=True, blank=True)  # for protection
    managing_tips = models.TextField(null=True, blank=True)  # for chronic or epidemic patients
    author = models.ForeignKey(User_Account, on_delete= models.SET_NULL, null=True,blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
