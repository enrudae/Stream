from django.contrib.auth.models import AbstractUser
from django.db import models
from Stream.yandex_s3_storage import ClientDocsStorage


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=100)
    image = models.FileField(storage=ClientDocsStorage(), null=True, blank=True)
    is_musician = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def become_musician(self):
        musician_profile = MusicianProfile.objects.create(user=self)
        self.is_musician = True
        self.save()
        return musician_profile

    def get_musician_subscriptions(self):
        user_subscriptions = Subscription.objects.filter(user=self).select_related('musician')
        return [subscription.musician for subscription in user_subscriptions]

    def __str__(self):
        return self.username


class MusicianProfile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='user', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    subscription_count = models.IntegerField(default=0)

    def update_subscription_count(self, increment=True):
        self.subscription_count += 1 if increment else -1
        self.save()

    class Meta:
        verbose_name = 'Профиль музыканта'
        verbose_name_plural = 'Профили музыкантов'


class Subscription(models.Model):
    subscription_date = models.DateTimeField(auto_now_add=True)
    musician = models.ForeignKey(MusicianProfile, verbose_name='Музыкант', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', related_name='subscriber',
                             on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'musician'],
                name='unique_user_musician'
            )
        ]
