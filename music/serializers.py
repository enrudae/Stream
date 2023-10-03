from rest_framework import serializers
from django.shortcuts import get_object_or_404
from user.serializers import MusicianProfileSerializer
from .models import Playlist, Track, Genre, Mood, FavoriteTrack, MusicianProfile, Album, LikeToAlbum


class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Playlist
        fields = '__all__'
        read_only_fields = ('track_count', 'duration_time', 'created_date')


class AlbumSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Album
        fields = '__all__'
        read_only_fields = ('track_count', 'duration_time', 'created_date', 'musician')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['musician'] = instance.musician.name
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        musician = MusicianProfile.objects.get(user=user)
        album = Album.objects.create(musician=musician, **validated_data)
        return album


class LikeToAlbumSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LikeToAlbum
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data['user']
        album = validated_data['album']
        existing_like = LikeToAlbum.objects.filter(user=user, album=album).exists()
        if existing_like:
            raise serializers.ValidationError('Like already exists.')

        like = LikeToAlbum.objects.create(user=user, album=album)
        return like


class TrackSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    album = serializers.CharField(required=False, allow_null=True, source='album.name')
    is_favorite = serializers.BooleanField(required=False)
    musician = MusicianProfileSerializer()

    class Meta:
        model = Track
        exclude = ('original_track', 'mood', 'genre')
        read_only_fields = ('track', 'duration', 'created_date', 'album', 'genre', 'mood', 'musician', 'is_favorite')


class TrackCreateModifySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Track
        exclude = ('duration', 'created_date', 'track')
        read_only_fields = ('musician',)

    def create(self, validated_data):
        user = self.context['request'].user
        musician = MusicianProfile.objects.get(user=user)
        track = Track.objects.create(musician=musician, **validated_data)
        return track


class FavoriteTrackSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    track = TrackSerializer(read_only=True)
    track_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = FavoriteTrack
        fields = '__all__'
        read_only_fields = ('like_date',)

    def create(self, validated_data):
        track_id = validated_data['track_id']
        user = validated_data['user']
        track = get_object_or_404(Track, id=track_id)
        favorite_track = FavoriteTrack.objects.get_or_create(user=user, track=track)
        return favorite_track
