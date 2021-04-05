from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    is_active = models.BooleanField(default=False, verbose_name='Активный пользователь')
    about_me = models.CharField(max_length=200, blank=True, null=True)
    subscribers = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='subscriptions')
    photo = models.ImageField(upload_to='photo', default='empty_photo.svg')
