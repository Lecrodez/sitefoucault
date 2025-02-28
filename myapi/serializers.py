import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import User, Survey, AnswerType, Answer, QuestionType, Question


class NameSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)

    def validate_name(self, value):
        """Общая валидация для имени и фамилии."""
        if not re.match(r'^[А-Яа-яЁё\s-]+$', value):
            raise serializers.ValidationError("Имя и фамилия должны содержать только русские буквы.")
        return value

    def validate_first_name(self, value):
        return self.validate_name(value)

    def validate_last_name(self, value):
        return self.validate_name(value)


class UserProfileSerializer(NameSerializer, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'roles', 'avatar']


class UserRegistrationSerializer(NameSerializer, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'roles', 'password']

    def create(self, validated_data):
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            roles=validated_data['roles']
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
        fields = ['value', 'question_type', 'options']


class SurveySerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    recipient_user = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Survey
        fields = ['title', 'description', 'questions', 'recipient_user']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        recipient_users_data = validated_data.pop('recipient_user')

        survey = Survey.objects.create(**validated_data)

        survey.recipient_user.set(recipient_users_data)

        for question_data in questions_data:
            Question.objects.create(survey=survey, **question_data)

        return survey



#


class QuestionTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionType
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'value', 'selected_options']

    def validate(self, data):
        question = data.get('question')
        question_type = question.question_type.name

        if question_type == 'текстовый' and not data.get('value'):
            raise serializers.ValidationError("Текстовый ответ обязателен для текстовых вопросов.")
        elif question_type in ['одиночный выбор', 'множественный выбор']:
            selected_options = data.get('selected_options', [])
            if not selected_options:
                raise serializers.ValidationError("Выберите хотя бы один вариант.")
            if question_type == 'одиночный выбор' and len(selected_options) > 1:
                raise serializers.ValidationError("Для одиночного выбора можно выбрать только один вариант.")

    def create(self, validated_data):
        # Если вопрос типа "одиночный выбор" или "множественный выбор", сохраняем выбранные варианты
        question = validated_data['question']
        question_type = question.question_type.name

        if question_type in ['одиночный выбор', 'множественный выбор']:
            selected_options = validated_data.pop('selected_options', [])
            # Здесь вы можете добавить логику для сохранения выбранных вариантов, если это необходимо

        return super().create(validated_data)


class AnswerTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerType
        fields = "__all__"
