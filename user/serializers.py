from rest_framework import serializers
from .models import Subscription, CustomUser, MusicianProfile
from django.shortcuts import get_object_or_404


class MusicianProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MusicianProfile
        exclude = ['user']
        read_only = ['created_date', 'subscription_count']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['name'] = instance.user.username
        return data


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
