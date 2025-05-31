from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('fetch-articles/', views.fetch_articles, name='fetch_articles'),
    path('recategorize-articles/', views.recategorize_articles, name='recategorize_articles'),
] 