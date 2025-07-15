from django.contrib import admin
from .models import Diseases_For_Ai

class Disease_AI_Admin(admin.ModelAdmin):
    list_display = ['disease_name']

admin.site.register(Diseases_For_Ai,Disease_AI_Admin)