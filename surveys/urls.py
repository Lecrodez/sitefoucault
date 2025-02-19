from django.contrib import admin
from django.urls import path, include

from surveys import views
from users.API_views import UserAPIView

urlpatterns = [
    path("", views.SurveysHome, name="home"),
]
