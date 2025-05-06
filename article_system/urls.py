from django.urls import path
from .views import *

urlpatterns = [
    path('create_article/',create_article,name='create_article'),
]