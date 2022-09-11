import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string

from core.models import CommonFields


# Create your models here.


class User(AbstractUser, CommonFields):
    """Authentication"""
    jwt_token_key = models.CharField(max_length=12, default=get_random_string)

    """Basic Info"""
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=False, unique=True, max_length=254, verbose_name="Email Address")
    current_country = models.CharField(max_length=255, null=True, blank=True, default='')

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

