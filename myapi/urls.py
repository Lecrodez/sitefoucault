from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import api
from .api import RegisterAPIView, UserProfileAPIView, UserProfileAPIUpdate, UserSurveysAPIView, SurveyCreateAPIView, \
    AnswerCreateAPIView

urlpatterns = [
    path('user/me/edit/', UserProfileAPIUpdate.as_view(), name='profile_edit'),
    path('user/me/', UserProfileAPIView.as_view(), name='profile'),
    path('my_surveys/', UserSurveysAPIView.as_view(), name='recieve_surveys'),
    path('drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('surveys_construct/', SurveyCreateAPIView.as_view(), name='survey-create'),
    path('surveys/<int:survey_id>/answers/', AnswerCreateAPIView.as_view(), name='answer-create'),
]