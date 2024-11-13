from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        verbose_name="Электронная почта",
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name="Имя пользователя",
        max_length=150,
    )
    last_name = models.CharField(
        verbose_name="Фамилия пользователя",
        max_length=150,
    )

    def __str__(self):
        return self.username