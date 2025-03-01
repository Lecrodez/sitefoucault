from django.urls import path, include
from .api import RegisterAPIView, UserProfileAPIView, UserProfileAPIUpdate, UserAvailableSurveysAPIView, \
    SurveyCreateAPIView, SurveyAnswerView, UserSurveysView, SurveyResponsesView, UserListAPIView

urlpatterns = [
    path('users/', UserListAPIView.as_view(), name="user_list"),  # Просмотр списка всех пользователей
    path('user/me/edit/', UserProfileAPIUpdate.as_view(), name='profile_edit'),  # Изменение данных пользователя
    path('user/me/', UserProfileAPIView.as_view(), name='profile'),  # Просмотр данных пользователя
    path('available_surveys/', UserAvailableSurveysAPIView.as_view(), name='receive_surveys'),  # Все входящие опросы
    path('available_surveys/<int:pk>/', UserAvailableSurveysAPIView.as_view(), name='receive_survey_detail'),  #
    # Входящий опрос
    path('my_surveys/', UserSurveysView.as_view(), name='created_surveys'),  # Просмотр созданных опросников
    path('surveys/<int:survey_id>/responses/', SurveyResponsesView.as_view(), name='survey-responses'),  # Просмотр
    # ответов на определенный опросник
    path('drf-auth/', include('rest_framework.urls')),  # Встроенные URL-адреса Django REST Framework для
    # аутентификации
    path('register/', RegisterAPIView.as_view(), name='api_register'),  # Регистрация пользователя
    path('surveys_construct/', SurveyCreateAPIView.as_view(), name='survey-create'),  # Создание опросника
    path('surveys/answers/', SurveyAnswerView.as_view(), name='answer-create')  # Ответ пользователя на опросник
]
