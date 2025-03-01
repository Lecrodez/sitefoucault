import re
from rest_framework import serializers

from .models import User, Survey, AnswerType, Answer, QuestionType, Question
import logging

logger = logging.getLogger("myapi")  # Подключение логгирования


class NameSerializer(serializers.Serializer):
    """
    Сериализатор для имени и фамилии.
    Включает общую валидацию для полей first_name и last_name.
    """

    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)

    def validate_name(self, value):
        """Общая валидация для имени и фамилии."""
        if not re.match(r'^[А-Яа-яЁё\s-]+$', value):
            logger.warning(f"Некорректное имя или фамилия: {value}")
            raise serializers.ValidationError("Имя и фамилия должны содержать только русские буквы.")
        return value

    def validate_first_name(self, value):
        """Валидация для поля first_name."""
        return self.validate_name(value)

    def validate_last_name(self, value):
        """Валидация для поля last_name."""
        return self.validate_name(value)


class UserProfileSerializer(NameSerializer, serializers.ModelSerializer):
    """
    Сериализатор для профиля пользователя.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'roles', 'avatar']


class UserRegistrationSerializer(NameSerializer, serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'roles', 'password']

    def create(self, validated_data):
        """
        Создает нового пользователя с хешированным паролем.
        """
        try:
            user = User(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                email=validated_data['email'],
                roles=validated_data['roles']
            )
            user.set_password(validated_data['password'])  # Хеширование пароля
            user.save()
            logger.info(f"Пользователь {user.email} успешно зарегистрирован.")
            return user

        except Exception as e:
            logger.error(f"Ошибка при регистрации пользователя: {e}")
            raise


class QuestionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вопроса.
    Используется для создания и отображения вопросов.
    """
    class Meta:
        model = Question
        fields = ['value', 'question_type', 'value']


class SurveySerializer(serializers.ModelSerializer):
    """
    Сериализатор для опросника.
    Включает вложенный сериализатор для вопросов (QuestionSerializer).
    Также добавляет получателей опросника.
    """
    questions = QuestionSerializer(many=True)
    recipient_user = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Survey
        fields = ['title', 'description', 'questions', 'recipient_user']

    def create(self, validated_data):
        """
        Создает опросник с вопросами и получателями.
        """
        try:
            questions_data = validated_data.pop('questions')
            recipient_users_data = validated_data.pop('recipient_user')

            survey = Survey.objects.create(**validated_data)

            survey.recipient_user.set(recipient_users_data)

            for question_data in questions_data:
                Question.objects.create(survey=survey, **question_data)

            logger.info(f"Опросник '{survey.title}' успешно создан пользователем {self.context['request'].user.email}.")
            return survey

        except Exception as e:
            logger.error(f"Ошибка при создании опросника: {e}")
            raise


class QuestionTypeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для типа вопроса.
    """
    class Meta:
        model = QuestionType
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    """
    Сериализатор для ответа на вопрос.
    """
    class Meta:
        model = Answer
        fields = ['value', 'question', 'answer_type']
        extra_kwargs = {
            'recipient_user': {'required': False}  # Делаем поле необязательным
        }

    def validate(self, data):
        """
        Валидация ответа в зависимости от типа вопроса.
        """
        question = data['question']
        answer_type = data['answer_type']
        value = data['value']

        if answer_type.name == "Текстовый":
            if not isinstance(value, str):
                logger.warning(f"Некорректный текстовый ответ: {value}")
                raise serializers.ValidationError("Ожидается текстовый ответ.")
        elif answer_type.name == "Численный":
            if not isinstance(value, (int, float)):
                logger.warning(f"Некорректный численный ответ: {value}")
                raise serializers.ValidationError("Ожидается численный ответ.")
        elif answer_type.name == "Одиночный выбор":
            if not (isinstance(value, str) and value in question.value):
                logger.warning(f"Некорректный одиночный выбор: {value}")
                raise serializers.ValidationError("Выбран недопустимый вариант ответа.")
        elif answer_type.name == "Множественный выбор":
            if not (isinstance(value, list) and all(v in question.value for v in value)):
                logger.warning(f"Некорректный множественный выбор: {value}")
                raise serializers.ValidationError("Выбраны недопустимые варианты ответа.")
            if len(value) < 1:
                logger.warning("Не выбран ни один вариант в множественном выборе.")
                raise serializers.ValidationError("Необходимо выбрать хотя бы один вариант.")

        return data


class SurveyAnswerSerializer(serializers.Serializer):
    """
    Сериализатор для ответа на опросник.
    Включает проверку, что пользователь является получателем опросника.
    """
    survey_id = serializers.PrimaryKeyRelatedField(queryset=Survey.objects.all(), required=True)
    answers = AnswerSerializer(many=True)

    def validate(self, data):
        """
        Проверяет, что пользователь является получателем опросника.
        """
        user = self.context['request'].user
        survey = data['survey_id']

        # Проверка, что пользователь является получателем опросника
        if user not in survey.recipient_user.all():
            logger.warning(f"Пользователь {user.email} не является получателем опросника {survey.id}.")
            raise serializers.ValidationError("Вы не являетесь получателем этого опросника.")

        logger.debug(f"Пользователь {user.email} успешно прошел валидацию для опросника {survey.id}.")

        return data

    def create(self, validated_data):
        """
        Создает ответы на вопросы опросника.
        """
        user = self.context['request'].user
        survey = validated_data['survey_id']
        answers_data = validated_data['answers']
        answers = []

        try:
            for answer_data in answers_data:
                answer_data['recipient_user'] = user
                answer = Answer.objects.create(**answer_data)
                answers.append(answer)

            logger.info(f"Пользователь {user.email} успешно ответил на опросник {survey.id}.")
            return answers
        except Exception as e:
            logger.error(f"Ошибка при создании ответов на опросник: {e}")
            raise


class AnswerDetailSerializer(serializers.ModelSerializer):
    """
    Cериализатор для отображения ответов на опросы
    """
    question = serializers.StringRelatedField()  # Отображаем текст вопроса
    recipient_user = serializers.StringRelatedField()  # Отображаем email получателя

    class Meta:
        model = Answer
        fields = ['id', 'question', 'value', 'recipient_user', 'answer_type']


class AnswerTypeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для типа ответа.
    """
    class Meta:
        model = AnswerType
        fields = "__all__"
