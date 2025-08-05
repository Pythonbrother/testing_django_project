from django.contrib import admin
from .models import Diseases_For_Ai, User_Disease_report

class Disease_AI_Admin(admin.ModelAdmin):
    list_display = ['pk','disease_name']

class report_admin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'disease']

admin.site.register(Diseases_For_Ai,Disease_AI_Admin)
admin.site.register(User_Disease_report, report_admin)