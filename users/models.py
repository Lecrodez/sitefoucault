from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # avatar = models.ImageField(upload_to="users/%Y/%m/%d", blank=True, null=True, verbose_name="Фотография")
    roles = models.ForeignKey('Roles', on_delete=models.PROTECT)


    def __str__(self):
        return self.username


class Roles(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name