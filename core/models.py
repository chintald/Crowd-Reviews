from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    email = models.EmailField(blank=False, max_length=254, verbose_name="Email Address")
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

