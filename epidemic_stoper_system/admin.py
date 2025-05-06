from django.contrib import admin
from .models import Epidemic

class Epidemic_Admin(admin.ModelAdmin):
    list_display = ['id','name']

admin.site.register(Epidemic, Epidemic_Admin)
