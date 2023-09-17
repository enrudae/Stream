from rest_framework import serializers
from .models import *
from user.serializers import MusicianProfileSerializer


class PostSerializer(serializers.ModelSerializer):
    musician = MusicianProfileSerializer()

    class Meta:
        model = Post
        fields = ('id', 'text', 'image', 'like_count', 'created_date', 'musician', 'track')


class PostCreateModifySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        exclude = ['created_date']
        read_only_fields = ('musician',)

    def create(self, validated_data):
        user = self.context['request'].user
        musician = MusicianProfile.objects.get(user=user)
        post = Post.objects.create(musician=musician, **validated_data)
        return post
