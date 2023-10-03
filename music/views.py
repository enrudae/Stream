from django.db.models import Prefetch, Count, Case, When
from rest_framework import generics, status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from permissions.permissions import IsMusician, IsMusicianCreator
from .models import Playlist, Track, TrackInPlaylist, Genre, Mood, FavoriteTrack, Album, LikeToAlbum
from .serializers import PlaylistSerializer, TrackSerializer, GenreSerializer, FavoriteTrackSerializer, \
    TrackCreateModifySerializer, AlbumSerializer, LikeToAlbumSerializer, MoodSerializer


class MoodGenreListView(APIView):
    def get(self, request, *args, **kwargs):
        moods = Mood.objects.all()
        genres = Genre.objects.all()

        mood_serializer = MoodSerializer(moods, many=True)
        genre_serializer = GenreSerializer(genres, many=True)

        return Response({
            'moods': mood_serializer.data,
            'genres': genre_serializer.data
        })


class TrackViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    serializer_class = TrackSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        user = self.request.user
        queryset = Track.objects.tracks_with_related_attributes()

        musician_id = self.request.query_params.get('musician_id')
        genre_id = self.request.query_params.get('genre_id')
        mood_id = self.request.query_params.get('mood_id')

        if musician_id:
            queryset = queryset.filter(musician=musician_id)
        if genre_id:
            queryset = queryset.filter(genre=genre_id)
        if mood_id:
            queryset = queryset.filter(mood_id=mood_id)

        return queryset.annotate(
            is_favorite=Count(Case(When(favorite_track__user=user, then=1)))
        )

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsMusician()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsMusicianCreator()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return TrackCreateModifySerializer
        return TrackSerializer


class FavoriteTrackViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    serializer_class = FavoriteTrackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return FavoriteTrack.objects.filter(user=user).prefetch_related(
            Prefetch('track', queryset=Track.objects.select_related('album', 'musician'))
        )


class PlaylistViewSet(ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Playlist.objects.filter(user=user)

    @action(methods=['get'], detail=False)
    def tracks(self, request, pk=None):
        playlist = self.get_object()
        tracks = playlist.tracks.select_related('album', 'musician')

        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def add_track(self, request, pk=None, track_id=None):
        playlist = self.get_object()
        track = get_object_or_404(Track, id=track_id)
        _, is_created = playlist.tracks.through.objects.get_or_create(playlist=playlist, track=track)
        if is_created:
            playlist.update_track_count_and_duration_time(track.duration, increment=True)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=True)
    def delete_track(self, request, pk=None, track_id=None):
        playlist = self.get_object()
        track = get_object_or_404(Track, id=track_id)
        existing_track = playlist.tracks.through.objects.filter(playlist=playlist, track=track).exists()

        if not existing_track:
            return Response({'detail': 'Track not exists in playlist.'}, status=status.HTTP_400_BAD_REQUEST)

        playlist.tracks.through.objects.get(playlist=playlist, track=track).delete()
        playlist.update_track_count_and_duration_time(track.duration, increment=False)
        return Response({'detail': 'Track deleted from playlist.'}, status=status.HTTP_200_OK)


class LikeToAlbumViewSet(mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = LikeToAlbumSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return LikeToAlbum.objects.filter(user=user)


class AlbumViewSet(ModelViewSet):
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Album.objects.all().select_related('musician')

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsMusician()]
        elif self.action in ['update', 'partial_update', 'destroy', 'add_track', 'delete_track']:
            return [IsAuthenticated(), IsMusicianCreator()]
        return super().get_permissions()

    @action(methods=['get'], detail=False)
    def tracks(self, request, pk=None):
        album = self.get_object()
        tracks = album.tracks.select_related('musician')
        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def add_track(self, request, pk=None, track_id=None):
        album = self.get_object()
        track = get_object_or_404(Track, id=track_id)
        if track.album:
            return Response({'detail': 'Track has already been added to some album.'}, status=status.HTTP_400_BAD_REQUEST)
        track.album = album
        track.save(update_fields=['album'])
        album.update_track_count_and_duration_time(track.duration, increment=True)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['delete'], detail=True)
    def delete_track(self, request, pk=None, track_id=None):
        album = self.get_object()
        track = get_object_or_404(Track, id=track_id)
        if track.album:
            track.album = None
            track.save(update_fields=['album'])
            album.update_track_count_and_duration_time(track.duration, increment=False)
        return Response({'detail': 'Track deleted from album.'}, status=status.HTTP_200_OK)
