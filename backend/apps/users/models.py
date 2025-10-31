from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    language_pref = models.CharField(max_length=10, default='en')

    def __str__(self):
        return self.username
