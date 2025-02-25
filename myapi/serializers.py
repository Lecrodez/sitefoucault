from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from .models import User, Survey, AnswerType, Answer, QuestionType, Question


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role_id', 'password']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role_id', 'password']

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            roles=validated_data['role_id']
        )
        user.set_password(validated_data['password'])  # Хеширование пароля
        user.save()
        return user


# class SurveySerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Survey
#         fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = "__all__"


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)  # Вложенный сериализатор для вопросов
    created_by = UserSerializer(read_only=True)  # Сериализатор для создателя опросника

    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'created_by', 'created_at', 'updated_at', 'questions']

    def create(self, validated_data):
        # Извлекаем данные для вопросов
        questions_data = validated_data.pop('questions')
        # Создаем опросник
        survey = Survey.objects.create(**validated_data)
        # Создаем вопросы
        for question_data in questions_data:
            Question.objects.create(survey=survey, **question_data)
        return survey


class QuestionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionType
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = "__all__"


class AnswerTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerType
        fields = "__all__"
