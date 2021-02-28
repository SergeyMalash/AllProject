from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    is_active = models.BooleanField(default=False, verbose_name='Активный пользователь')
