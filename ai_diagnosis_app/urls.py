from django.urls import path
from .views import *

urlpatterns = [
    path("",diagnosis,name="diagnosis"),
]