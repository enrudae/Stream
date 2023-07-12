from django.contrib.auth.models import AbstractUser
from django.db import models
from Stream.yandex_s3_storage import ClientDocsStorage


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    image = models.FileField(storage=ClientDocsStorage(), null=True, blank=True)
    is_musician = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class MusicianProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='user', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    subscription_count = models.IntegerField(default=0)

    def update_subscription_count(self, increment=True):
        self.subscription_count += 1 if increment else -1
        self.save()


class Subscription(models.Model):
    subscription_date = models.DateTimeField(auto_now_add=True)
    musician = models.ForeignKey(MusicianProfile, verbose_name='Музыкант', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', related_name='subscriber',
                             on_delete=models.CASCADE)
