import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils.crypto import get_random_string


class User(AbstractUser):
    """Authentication"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    jwt_token_key = models.CharField(max_length=12, default=get_random_string)
    username = models.CharField(max_length=20, unique=True)

    email = models.EmailField(blank=False, unique=True, max_length=254, verbose_name="Email Address")
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

