from django.urls import path
from .views import *
urlpatterns = [
    path("",home_view,name='home'),
    path('epidemic_insertion/',epidemic_insertion_view,name='epidemic_insertion'),
    path('examine_prevention_tip/',examine_prevention_tip,name="examine_prevention_tip"),
    path('examine_managing_tip/',examine_managing_tip,name='examine_managing_tip')
]