
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from . import models
from .models import Survey, User, Answer
from .serializers import UserRegistrationSerializer, SurveySerializer, QuestionSerializer, UserProfileSerializer, \
    AnswerSerializer


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


class AnswerCreateAPIView(CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        survey_id = self.kwargs['survey_id']

        try:
            survey = Survey.objects.get(pk=survey_id)
        except Survey.DoesNotExist:
            raise NotFound("Опрос не найден.")

            # Убедитесь, что вопрос принадлежит этому опросу
        question = serializer.validated_data['question']
        if question.survey != survey:
            raise NotFound("Вопрос не принадлежит этому опросу.")

        # Автоматически назначаем текущего пользователя как ответчика
        serializer.save(user=self.request.user)


# class AnswerViewSet(CreateAPIView):
#     queryset = Answer.objects.all()
#     serializer_class = AnswerSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
