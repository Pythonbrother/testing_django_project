from django.urls import path
from .views import *
urlpatterns = [
    path("",home_view,name='home'),
    path('epidemic_insertion/',epidemic_insertion_view,name='epidemic_insertion'),
    path('examine_prevention_tip/<int:epidemic_id>',examine_prevention_tip,name="examine_prevention_tip"),
    path('examine_managing_tip/<int:epidemic_id>',examine_managing_tip,name='examine_managing_tip'),
    path('epidemic_intro/',epidemic_intro, name='epidemic_intro'),
    path('epidemic_detail/<int:epidemic_id>',epidemic_detail,name='epidemic_detail'),
    path('my_account/',my_account,name='my_account'),
    path('test/<int:article_pk>',test,name='test'),
]