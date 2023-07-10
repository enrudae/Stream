from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Playlist, Track, TrackInPlaylist
from .serializers import PlaylistSerializer, TrackSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class PlaylistViewSet(ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        return Playlist.objects.filter(user=user)

    @action(methods=['post'], detail=True)
    def add_track(self, request, pk=None, track_id=None):
        playlist = self.get_object()

        if track_id:
            track = Track.objects.get_object_or_404(id=track_id)
            TrackInPlaylist.objects.create(playlist=playlist, track=track)
            return Response({'detail': 'Track added to playlist.'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid track ID.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def tracks(self, request, pk=None):
        playlist = self.get_object()
        tracks_in_playlist = TrackInPlaylist.objects.filter(playlist=playlist)
        tracks = [track_in_playlist.track for track_in_playlist in tracks_in_playlist]

        serializer = TrackSerializer(tracks, many=True)
        return Response(serializer.data)
