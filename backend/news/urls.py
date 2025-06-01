from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.home, name='home'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('register/', views.register1, name='register'),
    path('register2/', views.register2, name='register2'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('send-email/', views.send_email, name='send_email'),
    path('send-test-email/', views.send_test_email, name='send_test_email'),
    path('test-email/', views.test_email_page, name='test_email_page'),
    path('load-more/', views.load_more_articles, name='load_more_articles'),
    path('test-email-digest/', views.test_email_digest, name='test_email_digest'),
    path('test-digest-page/', views.test_digest_page, name='test_digest_page'),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/preferences/', views.update_preferences, name='update_preferences'),
    path('profile/notifications/', views.update_notifications, name='update_notifications'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    path('profile/change-password/', views.change_password, name='change_password'),
]
