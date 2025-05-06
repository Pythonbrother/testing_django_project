from django.db import models
from account_system.models import User_Account

class Epidemic(models.Model):
    name = models.CharField(max_length=30)
    symptoms = models.TextField()
    prevention_tips = models.TextField()
    managing_tips = models.TextField()
    creator = models.ForeignKey(User_Account, on_delete= models.SET_NULL, null=True,blank=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
