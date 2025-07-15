from django.db import models

class Diseases_For_Ai(models.Model):
    disease_name = models.CharField(max_length=50, null=True, blank=True)
    topic = models.TextField(null=True, blank=True)
    symptoms = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.disease_name
