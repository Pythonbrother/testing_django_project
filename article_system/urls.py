from django.urls import path
from .views import *

urlpatterns = [
    path('create_article/',create_article,name='create_article'),
    path('article_intro/',article_intro,name='article_intro'),
    path('article_detail/<int:article_pk>',article_detail,name='article_detail'),
    path('update_article/<int:pk>',update_article.as_view(),name='update_article'),
    path('delete_article/<int:pk>', delete_article.as_view(), name='delete_article')
]