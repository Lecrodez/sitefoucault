from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView, UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Survey, User, Answer
from .serializers import UserRegistrationSerializer, SurveySerializer, UserProfileSerializer, SurveyAnswerSerializer, \
    AnswerDetailSerializer
import logging

logger = logging.getLogger("myapi")  # Подключение логгирования


class UserListAPIView(ListAPIView):
    """
    Представление для просмотра списка всех пользователей
    """
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        logger.info(f"Пользователь {self.request.user.email} запросил список всех пользователей.")
        return User.objects.all()


class UserProfileAPIView(ListAPIView):
    """
    Представление для просмотра профиля текущего пользователя.
    """
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        logger.info(f"Пользователь {self.request.user.email} запросил свой профиль.")
        return User.objects.filter(id=self.request.user.id)


class RegisterAPIView(CreateAPIView):
    """
    Представление для регистрации нового пользователя.
    """
    serializer_class = UserRegistrationSerializer


class SurveyCreateAPIView(CreateAPIView):
    """
    Представление для создания опросника.
    """
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # Автоматически назначаем текущего пользователя как создателя опросника
        serializer.save(sender_user=self.request.user)


class UserProfileAPIUpdate(UpdateAPIView):
    """
    Представление для обновления профиля текущего пользователя.
    Позволяет авторизованному пользователю редактировать свои данные.
    """
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        logger.info(f"Пользователь {self.request.user.email} запросил обновление своего профиля.")
        return self.request.user

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            logger.info(f"Пользователь {self.request.user.email} успешно обновил свой профиль.")
            return response
        except Exception as e:
            logger.error(f"Ошибка при обновлении профиля пользователя: {e}")
            raise


class UserSurveysView(APIView):
    """
    Представление для просмотра опросников, созданных текущим пользователем.
    """
    def get(self, request, *args, **kwargs):
        # Получаем текущего пользователя
        user = request.user
        logger.info(f"Пользователь {user.email} запросил список своих опросников.")

        # Фильтруем опросы, где текущий пользователь является отправителем
        surveys = Survey.objects.filter(sender_user=user)

        # Сериализуем данные
        serializer = SurveySerializer(surveys, many=True)

        # Возвращаем ответ
        logger.debug(f"Найдено {len(surveys)} опросников для пользователя {user.email}.")
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAvailableSurveysAPIView(ListAPIView):
    """
    Представление для просмотра входящих опросников.
    """
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        logger.info(f"Пользователь {user.email} запросил список входящих опросников.")
        return Survey.objects.filter(recipient_user=self.request.user)

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос.
        Если передан ID опроса, возвращает детали опроса.
        Иначе возвращает список опросников.
        """
        # Проверяем, передан ли ID опроса
        survey_id = kwargs.get('pk')
        if survey_id is not None:
            logger.debug(f"Пользователь {request.user.email} запросил детали опросника с ID {survey_id}.")
            # Если ID опроса передан, возвращаем конкретный опрос
            return self.retrieve(request, *args, **kwargs)
        else:
            logger.debug(f"Пользователь {request.user.email} запросил список входящих опросников.")
            # Если ID не передан, возвращаем список опросов
            return self.list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Возвращает детали конкретного опроса по его ID.
        """
        try:
            queryset = self.get_queryset()
            obj = get_object_or_404(queryset, pk=kwargs['pk'])
            serializer = self.get_serializer(obj)
            logger.info(f"Детали опросника {obj.id} успешно возвращены пользователю {request.user.email}.")
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Ошибка при получении деталей опросника: {e}")
            raise


class SurveyAnswerView(APIView):
    """
    Представление для отправки ответов на опросник.
    - POST: Принимает ответы на вопросы опросника и сохраняет их.
    """
    def post(self, request, *args, **kwargs):
        logger.info(f"Пользователь {request.user.email} отправил ответы на опросник.")

        serializer = SurveyAnswerSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Ответы пользователя {request.user.email} успешно сохранены.")
            return Response({"message": "Ответы успешно сохранены."}, status=status.HTTP_201_CREATED)

        logger.warning(f"Ошибки при валидации ответов пользователя {request.user.email}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Представление которое возвращает ответы на опросник, созданный текущим пользователем
class SurveyResponsesView(APIView):
    """
    Представление для просмотра ответов на опросник, созданный текущим пользователем.
    """
    def get(self, request, survey_id, *args, **kwargs):
        # Получаем текущего пользователя
        user = request.user
        logger.info(f"Пользователь {user.email} запросил ответы на опросник с ID {survey_id}.")

        # Проверяем, что опросник принадлежит текущему пользователю
        try:

            survey = Survey.objects.get(id=survey_id, sender_user=user)
            # Получаем все ответы на вопросы этого опросника
            answers = Answer.objects.filter(question__survey=survey)
            # Сериализуем данные
            serializer = AnswerDetailSerializer(answers, many=True)

            logger.debug(f"Найдено {len(answers)} ответов на опросник {survey_id}.")
            # Возвращаем ответ
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Survey.DoesNotExist:
            logger.warning(f"Опросник {survey_id} не найден или пользователь {user.email} не является его создателем.")
            return Response({"error": "Опросник не найден или вы не являетесь его создателем."},
                            status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.error(f"Ошибка при получении ответов на опросник: {e}")
            raise