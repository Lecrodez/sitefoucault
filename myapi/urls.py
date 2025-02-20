from django.urls import path
from . import api

urlpatterns = [
    path('users/', api.UserListAPIView.as_view(), name='api_users'),
    path('roles/', api.RolesListAPIView.as_view(), name='api_roles'),
]