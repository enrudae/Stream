from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Subscription
from .serializers import SubscriptionSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class SubscriptionViewSet(ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        musician = instance.musician
        musician.update_subscription_count(increment=False)
        return super().destroy(request, *args, **kwargs)

