from django.urls import path, include
from . import api
from .api import SurveyCreateAPIView, RegisterAPIView, UserProfileAPIView, UserProfileAPIUpdate, UserSurveysAPIView

urlpatterns = [
    path('user/me/edit/', UserProfileAPIUpdate.as_view(), name='profile_edit'),
    path('user/me/', UserProfileAPIView.as_view(), name='profile'),
    path('my_surveys/', UserSurveysAPIView.as_view(), name='recieve_surveys'),
    path('drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('surveys_construct/', SurveyCreateAPIView.as_view(), name='survey-create'),
]