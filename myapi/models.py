from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=30, blank=True, verbose_name="Фамилия")
    username = None
    email = models.EmailField(unique=True, verbose_name="E-mail", db_index=True)
    avatar = models.ImageField(upload_to="users/%Y/%m/%d", blank=True, null=True, verbose_name="Фотография", default="default/placeholder.png")
    roles = models.ForeignKey('Roles', on_delete=models.PROTECT, blank=False, verbose_name="Роль", related_name="role_id")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Roles(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'role'
        verbose_name_plural = 'roles'


class Survey(models.Model):
    title = models.CharField(max_length=40, verbose_name="Заголовок", db_index=True)
    description = models.CharField(max_length=255, verbose_name="Описание")
    sender_user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Отправитель", related_name="sender_id")
    recipient_user = models.ManyToManyField('User', verbose_name="Получатель", related_name="recipient_id")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    value = models.CharField(max_length=255, verbose_name="Вопрос", db_index=True)
    question_type = models.ForeignKey("QuestionType", on_delete=models.CASCADE, verbose_name="Тип вопроса", related_name="question_type_id")
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    options = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.value


class QuestionType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название типа вопроса", db_index=True)

    def __str__(self):
        return self.name


class Answer(models.Model):
    value = models.CharField(max_length=255, verbose_name="Ответ", db_index=True)
    answer_type = models.ForeignKey("AnswerType", on_delete=models.CASCADE, related_name="answer_type_id")
    recipient_user = models.ForeignKey("User", on_delete=models.PROTECT, related_name="recipient_user_id")
    question = models.OneToOneField("Question", on_delete=models.CASCADE, related_name="question_id")
    selected_options = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.value


class AnswerType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название типа ответа", db_index=True)

    def __str__(self):
        return self.name

