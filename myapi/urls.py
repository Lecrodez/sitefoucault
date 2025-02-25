from django.urls import path, include
from . import api
from .api import SurveyCreateView

urlpatterns = [
    path('users/', api.UserListAPIView.as_view(), name='api_users'),
    path('drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('register/', api.RegisterAPIView.as_view(), name='api_register'),
    path('surveys/', SurveyCreateView.as_view(), name='survey-create'),
]