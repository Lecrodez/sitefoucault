from rest_framework import permissions
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView

from . import serializers
from . import models
from .models import Survey, User
from .serializers import UserRegistrationSerializer, SurveySerializer, QuestionSerializer, UserProfileSerializer


class UserProfileAPIView(ListAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class RegisterAPIView(CreateAPIView):
    serializer_class = UserRegistrationSerializer


class SurveyCreateAPIView(ListCreateAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        # Автоматически назначаем текущего пользователя как создателя опросника
        serializer.save(sender_user=self.request.user)


class UserProfileAPIUpdate(UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return self.request.user


class UserSurveysAPIView(ListAPIView):
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Survey.objects.filter(recipient_user=self.request.user)