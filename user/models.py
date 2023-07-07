from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    is_musician = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class MusicianProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    musician_name = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_created=True)
    subscription_count = models.IntegerField(default=0)
