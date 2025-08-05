from django.db import models
from account_system.models import User_Account
from django.utils import timezone
class Diseases_For_Ai(models.Model):
    disease_name = models.CharField(max_length=50, null=True, blank=True, unique=True)
    topic = models.TextField(null=True, blank=True)
    #symptoms = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.disease_name

class User_Disease_report(models.Model):
    user = models.ForeignKey(User_Account, on_delete=models.SET_NULL,null=True, blank=True)
    disease = models.ForeignKey(Diseases_For_Ai, on_delete=models.SET_NULL, null=True, blank=True)
    created_time = models.DateTimeField(default=timezone.now, editable=True)

    def __str__(self):
        return str(self.pk)