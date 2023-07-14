from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from blog.models import *
from blog.serializers import PostSerializer, PostCreateSerializer


class PostsAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)


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


class MusicianPostsAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        musician_id = self.kwargs.get('pk', None)
        return Post.objects.filter(musician=musician_id)


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
