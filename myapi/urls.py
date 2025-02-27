from django.urls import path, include
from . import api
from .api import SurveyCreateAPIView, UserProfileAPIUpdate, RegisterAPIView, UserProfileAPIView

urlpatterns = [
    path('user/', UserProfileAPIView.as_view(), name='api_users'),
    path('user/<int:pk>/', UserProfileAPIUpdate.as_view(), name='user_upd'),
    path('drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('surveys_construct/', SurveyCreateAPIView.as_view(), name='survey-create'),
]