from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from blog.views import PostViewSet
from music.views import PlaylistViewSet, MoodGenreListView, FavoriteTrackViewSet, TrackViewSet, AlbumViewSet, \
    LikeToAlbumViewSet
from user.views import SubscriptionViewSet, CustomUserAPIView, MusicianProfileAPIView
from rest_framework import routers
from .yasg import urlpatterns as doc_urls

router = routers.DefaultRouter()
router.register('playlists', PlaylistViewSet, basename='playlist')
router.register('subscriptions', SubscriptionViewSet, basename='subscription')
router.register('favorites', FavoriteTrackViewSet, basename='favorite')
router.register('tracks', TrackViewSet, basename='track')
router.register('albums', AlbumViewSet, basename='album')
router.register('favorite-albums', LikeToAlbumViewSet, basename='favorite-album')
router.register('posts', PostViewSet, basename='post')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/register/', include('djoser.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/', include(router.urls)),

    path('api/playlists/<int:playlist_id>/add_track/<int:track_id>/', PlaylistViewSet.as_view({'post': 'add_track'}),
         name='playlist-add-track'),
    path('api/playlists/<int:playlist_id>/delete_track/<int:track_id>/', PlaylistViewSet.as_view({'delete': 'delete_track'}),
         name='playlist-delete-track'),
    path('api/playlists/<int:playlist_id>/tracks/', PlaylistViewSet.as_view({'get': 'tracks'}), name='playlist-tracks'),
    path('api/user/', CustomUserAPIView.as_view(), name='user-detail'),
    path('api/attributes/', MoodGenreListView.as_view(), name='attributes-list'),
    path('api/create_musician/', MusicianProfileAPIView.as_view(), name='create_musician'),

]

urlpatterns += doc_urls
