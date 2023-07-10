from rest_framework import serializers
from .models import Playlist, Track
from drf_extra_fields.fields import Base64ImageField


class PlaylistSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Playlist
        exclude = []
        read_only_fields = ('track_count', 'duration_time', 'created_date')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = instance.user.username
        return data


class TrackSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Track
        exclude = []
        read_only_fields = ('track', 'duration', 'created_date', 'album', 'genre', 'mood', 'musician')
