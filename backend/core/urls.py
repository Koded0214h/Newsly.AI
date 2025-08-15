from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

urlpatterns = [
    # Auth
    path("auth/register/", views.RegisterView.as_view(), name="auth-register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="auth-login"),      # returns access & refresh
    path("auth/refresh/", TokenRefreshView.as_view(), name="auth-refresh"),

    # User
    path("users/me/", views.MeView.as_view(), name="users-me"),
    path("users/preferences/", views.PreferenceView.as_view(), name="users-preferences"),
    
    # News
    path("feed/", views.PersonalizedFeedView.as_view(), name="personalized-feed"),
]
