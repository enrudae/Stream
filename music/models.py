from datetime import timedelta
from django.db import models
from django.contrib.auth import get_user_model
from django.core.files.storage import FileSystemStorage
from user.models import MusicianProfile
from Stream.yandex_s3_storage import ClientDocsStorage
from music.tasks import process_and_upload_track

CustomUser = get_user_model()


class Mood(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class TrackCountDurationMixin(models.Model):
    track_count = models.PositiveIntegerField(default=0)
    duration_time = models.DurationField(default=timedelta(seconds=0))

    class Meta:
        abstract = True

    def update_track_count_and_duration_time(self, duration, increment=True):
        if increment:
            self.track_count += 1
            self.duration_time += duration
        else:
            self.track_count -= 1
            self.duration_time -= duration
        self.save(update_fields=['track_count', 'duration_time'])


class Album(TrackCountDurationMixin, models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(storage=ClientDocsStorage(), null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    musician = models.ForeignKey(MusicianProfile, verbose_name='Музыкант', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class LikeToAlbum(models.Model):
    like_date = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey(Album, verbose_name='Альбом', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)


class TrackManager(models.Manager):
    def tracks_with_related_attributes(self):
        return self.get_queryset().select_related('musician', 'genre', 'album', 'mood')


class Track(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(storage=ClientDocsStorage(), null=True, blank=True)
    original_track = models.FileField(storage=FileSystemStorage(), upload_to='Stream/media/tracks/original/', null=True, blank=True)
    track = models.FileField(storage=ClientDocsStorage(), null=True, blank=True)
    duration = models.DurationField(default=timedelta(seconds=0))
    created_date = models.DateTimeField(auto_now_add=True)

    musician = models.ForeignKey(MusicianProfile, verbose_name='Создатель', on_delete=models.CASCADE, db_index=True)
    album = models.ForeignKey(Album, verbose_name='Альбом', related_name='tracks', on_delete=models.SET_NULL, blank=True, null=True, db_index=True)
    genre = models.ForeignKey(Genre, verbose_name='Жанр', on_delete=models.SET_NULL, blank=True, null=True, db_index=True)
    mood = models.ForeignKey(Mood, verbose_name='Настроение', on_delete=models.SET_NULL, blank=True, null=True, db_index=True)

    objects = TrackManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.original_track:
            process_and_upload_track.delay(self.id)


class Playlist(TrackCountDurationMixin, models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField(storage=ClientDocsStorage(), null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)
    tracks = models.ManyToManyField(Track, through='TrackInPlaylist')

    def __str__(self):
        return self.name


class FavoriteTrack(models.Model):
    like_date = models.DateTimeField(auto_now_add=True)
    track = models.ForeignKey(Track, verbose_name='Трек', related_name='favorite_track', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='Пользователь', on_delete=models.CASCADE)


class TrackInPlaylist(models.Model):
    playlist = models.ForeignKey(Playlist, verbose_name='Плейлист', on_delete=models.CASCADE)
    track = models.ForeignKey(Track, verbose_name='Трек', on_delete=models.CASCADE)
