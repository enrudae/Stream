from rest_framework import serializers
from .models import *


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ["is_deleted", "like_count"]
        read_only_fields = ('musician',)

    def create(self, validated_data):
        user = self.context['request'].user
        musician = MusicianProfile.objects.get(user=user)
        post = Post.objects.create(musician=musician, **validated_data)
        return post

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text", instance.text)
        instance.image = validated_data.get("image", instance.image)
        instance.track = validated_data.get("track", instance.track)
        instance.save()
        return instance
