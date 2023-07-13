import rest_framework.viewsets
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from blog.models import *
from blog.permissions import IsOwner, IsOwnerOrReadOnly, IsAuthenticatedAndSafe
from blog.serializers import PostSerializer, PostCreateSerializer


# Get all posts
class PostsAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)


# Get and Delete post by id
class PostListDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def check_permissions(self, request):
        super().check_permissions(request)
        if request.method in SAFE_METHODS:
            return True
        instance = self.get_object()
        if instance.musician.user != request.user:
            raise PermissionDenied(detail=("Cannot delete other people posts",))


# Get all musician's posts
class MusicianPostsAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        musician_id = self.kwargs.get('pk', None)
        return Post.objects.filter(musician=musician_id)


# Create new post
class NewMusicianPostAPIView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()

    def check_permissions(self, request):
        super().check_permissions(request)
        if not request.user.is_musician:
            raise PermissionDenied(detail=("Only musicians can create posts",))


class ModifyMusicianPostAPIView(generics.UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()

    def check_permissions(self, request):
        super().check_permissions(request)
        if not request.user.is_musician:
            raise PermissionDenied(detail=("Only musicians can modify posts",))

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.musician.user:
            return Response({'Error': 'Cannot modify others posts'})
        serializer = PostCreateSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
