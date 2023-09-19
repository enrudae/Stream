from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Subscription
from .serializers import SubscriptionSerializer, CustomUserSerializer, MusicianProfileSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import mixins, viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class SubscriptionViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(user=user).select_related('musician')

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        musician = instance.musician
        musician.update_subscription_count(increment=False)
        return super().destroy(request, *args, **kwargs)


class CustomUserAPIView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class MusicianProfileAPIView(generics.CreateAPIView):
    serializer_class = MusicianProfileSerializer
    permission_classes = [IsAuthenticated]
