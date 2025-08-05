from django.urls import path
from .views import *

urlpatterns = [
    path("",diagnosis,name="diagnosis"),
    path("report/",show_report, name='show_report'),
    path('be_report/',be_report, name='be_report')
]