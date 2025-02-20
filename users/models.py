from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True, )
    last_name = models.CharField(max_length=30, blank=True, )
    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="users/%Y/%m/%d", blank=True, null=True, verbose_name="Фотография", default="default/placeholder.png")
    roles = models.ForeignKey('Roles', on_delete=models.PROTECT, blank=False)

    USERNAME_FIELD = 'email'  # Используем email как уникальный идентификатор
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='users_user_set',  # Уникальное имя для users.User
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='users_user_permissions_set',  # Уникальное имя для users.User
        blank=True,
    )


class Roles(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'role'
        verbose_name_plural = 'roles'


