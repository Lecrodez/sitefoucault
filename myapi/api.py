from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from . import serializers
from . import models
from .serializers import UserRegistrationSerializer


class UserListAPIView(ListAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        return models.User.objects.all()


class RolesListAPIView(ListAPIView):
    serializer_class = serializers.RolesSerializers

    def get_queryset(self):
        return models.Roles.objects.all()


class RegisterAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer

