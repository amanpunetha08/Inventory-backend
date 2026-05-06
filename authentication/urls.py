from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import google_login

urlpatterns = [
    path('google/', google_login, name='google-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
