from rest_framework import serializers
from .models import Subscription, CustomUser, MusicianProfile
from django.shortcuts import get_object_or_404
from django.db import IntegrityError


class CustomUserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'image', 'is_musician', 'date_joined']
        read_only = ['email', 'date_joined']


class MusicianProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MusicianProfile
        exclude = ['created_date']
        read_only = ['subscription_count']

    def create(self, validated_data):
        user = validated_data['user']
        existing_subscription = MusicianProfile.objects.filter(user=user).exists()
        if existing_subscription:
            raise serializers.ValidationError('MusicianProfile already exists.')

        musician_profile = user.become_musician()
        return musician_profile


class SubscriptionSerializer(serializers.ModelSerializer):
    musician = MusicianProfileSerializer(read_only=True)
    musician_id = serializers.IntegerField(write_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        exclude = []

    def create(self, validated_data):
        musician_id = validated_data['musician_id']
        user = validated_data['user']
        musician = get_object_or_404(MusicianProfile, id=musician_id)

        try:
            subscription = Subscription.objects.create(musician=musician, user=user)
            musician.update_subscription_count(increment=True)
            return subscription
        except IntegrityError:
            raise serializers.ValidationError('Subscription already exists.')
