from django.db import models
from user.models import CustomUser, MusicianProfile
from Stream.yandex_s3_storage import ClientDocsStorage
from datetime import timedelta


class Mood(models.Model):
    name = models.CharField(max_length=25)


class Genre(models.Model):
    name = models.CharField(max_length=25)
    image = models.FileField(storage=ClientDocsStorage(), null=True, blank=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255, blank=True)
    track_count = models.IntegerField(default=0)
    duration_time = models.DurationField(default=timedelta(seconds=0))
    image = models.FileField(storage=ClientDocsStorage(), null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    musician = models.ForeignKey(MusicianProfile, verbose_name='Музыкант', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class LikeToAlbum(models.Model):
    like_date = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey(Album, verbose_name='Альбом', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)


class Playlist(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255, blank=True)
    track_count = models.IntegerField(default=0)
    duration_time = models.DurationField(default=timedelta(seconds=0))
    image = models.FileField(storage=ClientDocsStorage(), null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)

    def update_track_count_and_duration_time(self, duration, increment=True):
        if increment:
            self.track_count += 1
            self.duration_time += duration
        else:
            self.track_count -= 1
            self.duration_time -= duration
        self.save(update_fields=['track_count', 'duration_time'])

    def __str__(self):
        return self.name


class Track(models.Model):
    name = models.CharField(max_length=50)
    image = models.FileField(storage=ClientDocsStorage(), null=True, blank=True)
    track = models.FileField(storage=ClientDocsStorage())
    duration = models.DurationField()
    created_date = models.DateTimeField(auto_now_add=True)

    musician = models.ForeignKey(MusicianProfile, verbose_name='Создатель', on_delete=models.CASCADE)
    album = models.ForeignKey(Album, verbose_name='Альбом', on_delete=models.SET_NULL, blank=True, null=True)
    genre = models.ForeignKey(Genre, verbose_name='Жанр', on_delete=models.SET_NULL, blank=True, null=True)
    mood = models.ForeignKey(Mood, verbose_name='Настроение', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name


class FavoriteTrack(models.Model):
    like_date = models.DateTimeField(auto_now_add=True)
    track = models.ForeignKey(Track, verbose_name='Трек', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)


class TrackInPlaylist(models.Model):
    playlist = models.ForeignKey(Playlist, verbose_name='Плейлист', on_delete=models.CASCADE)
    track = models.ForeignKey(Track, verbose_name='Трек', on_delete=models.CASCADE)
