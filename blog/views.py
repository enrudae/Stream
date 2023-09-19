from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from blog.models import *
from blog.serializers import PostSerializer, PostCreateModifySerializer
from rest_framework.viewsets import ModelViewSet
from permissions.permissions import IsMusician, IsMusicianCreator
from rest_framework import mixins, viewsets


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Post.objects.all().select_related('musician')
        user = self.request.user
        musician_id = self.request.query_params.get('musician_id')
        feed = self.request.query_params.get('feed')

        if feed:
            musicians = user.get_musician_subscriptions()
            posts_in_feed = queryset.filter(musician__in=musicians)
            return posts_in_feed

        if musician_id:
            queryset = queryset.filter(musician=musician_id)

        return queryset

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsMusician()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsMusicianCreator()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return PostCreateModifySerializer
        return PostSerializer
