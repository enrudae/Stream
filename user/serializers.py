from rest_framework import serializers
from .models import Subscription, CustomUser, MusicianProfile
from django.shortcuts import get_object_or_404


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
        exclude = []
        read_only = ['created_date', 'subscription_count']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['name'] = instance.user.username
        return data

    def create(self, validated_data):
        user = validated_data['user']
        existing_subscription = MusicianProfile.objects.filter(user=user).exists()
        if existing_subscription:
            raise serializers.ValidationError('MusicianProfile already exists.')

        subscription = MusicianProfile.objects.create(user=user)
        user.become_musician()
        return subscription


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
        existing_subscription = Subscription.objects.filter(user=user, musician=musician).exists()
        if existing_subscription:
            raise serializers.ValidationError('Subscription already exists.')

        subscription = Subscription.objects.create(musician=musician, user=user)
        musician.update_subscription_count(increment=True)
        return subscription
