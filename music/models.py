from django.db import models
from user.models import CustomUser, MusicianProfile
from Stream.yandex_s3_storage import ClientDocsStorage


class Mood(models.Model):
    name = models.CharField(max_length=25)


class Genre(models.Model):
    name = models.CharField(max_length=25)


class Album(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255, blank=True)
    track_count = models.IntegerField(default=0)
    duration_time = models.DurationField()
    image = models.FileField(storage=ClientDocsStorage(), null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    musician = models.ForeignKey(MusicianProfile, verbose_name='Музыкант', on_delete=models.CASCADE)


class LikeToAlbum(models.Model):
    like_date = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey(Album, verbose_name='Альбом', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)


class Playlist(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255, blank=True)
    track_count = models.IntegerField(default=0)
    duration_time = models.DurationField()
    image = models.FileField(storage=ClientDocsStorage(), null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_favourites = models.BooleanField(default=False)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)


class Track(models.Model):
    name = models.CharField(max_length=50)
    image = models.FileField(storage=ClientDocsStorage(), null=True, blank=True)
    track = models.FileField(storage=ClientDocsStorage(), null=True, blank=True)
    duration = models.DurationField()
    created_date = models.DateTimeField(auto_now_add=True)

    musician = models.ForeignKey(MusicianProfile, verbose_name='Создатель', on_delete=models.CASCADE)
    album = models.ForeignKey(Album, verbose_name='Альбом', on_delete=models.SET_NULL, blank=True, null=True)
    genre = models.ForeignKey(Genre, verbose_name='Жанр', on_delete=models.SET_NULL, blank=True, null=True)
    mood = models.ForeignKey(Mood, verbose_name='Настроение', on_delete=models.SET_NULL, blank=True, null=True)


class TrackInPlaylist(models.Model):
    playlist = models.ForeignKey(Playlist, verbose_name='Плейлист', on_delete=models.CASCADE)
    track = models.ForeignKey(Track, verbose_name='Трек', on_delete=models.CASCADE)
