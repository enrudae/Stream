from django.db import models
from django.contrib.auth import get_user_model
from music.models import Track
from user.models import MusicianProfile
from Stream.yandex_s3_storage import ClientDocsStorage

CustomUser = get_user_model()


class Post(models.Model):
    text = models.TextField(max_length=255)
    image = models.ImageField(storage=ClientDocsStorage(), null=True, blank=True)
    like_count = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    musician = models.ForeignKey(MusicianProfile, verbose_name='Музыкант', on_delete=models.CASCADE)
    track = models.ForeignKey(Track, verbose_name='Трек', on_delete=models.SET_NULL, blank=True, null=True)

    def update_like_count(self, increment=True):
        self.like_count += 1 if increment else -1
        self.save(update_fields=['like_count'])


class CommentInPost(models.Model):
    text = models.TextField(max_length=255)
    image = models.ImageField(storage=ClientDocsStorage(), null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, verbose_name='Пост', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)


class LikeInPost(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, verbose_name='Пост', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)
