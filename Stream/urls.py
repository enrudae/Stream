from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from blog.views import PostsAPIView, PostListDestroyAPIView, MusicianPostsAPIView, NewMusicianPostAPIView, \
    ModifyMusicianPostAPIView
from music.views import PlaylistViewSet, GenreAPIView, FavoriteTrackViewSet, TrackViewSet
from user.views import SubscriptionViewSet, CustomUserAPIView, MusicianProfileAPIView
from rest_framework import routers
from .yasg import urlpatterns as doc_urls

router = routers.DefaultRouter()
router.register('playlists', PlaylistViewSet, basename='playlist')
router.register('subscriptions', SubscriptionViewSet, basename='subscription')
router.register('favorites', FavoriteTrackViewSet, basename='favorite')
router.register('tracks', TrackViewSet, basename='track')


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/register/', include('djoser.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/', include(router.urls)),
    path('api/playlists/<int:pk>/add_track/<int:track_id>/', PlaylistViewSet.as_view({'post': 'add_track'}), name='playlist-add-track'),
    path('api/playlists/<int:pk>/delete_track/<int:track_id>/', PlaylistViewSet.as_view({'delete': 'delete_track'}), name='playlist-delete-track'),
    path('api/playlists/<int:pk>/tracks/', PlaylistViewSet.as_view({'get': 'tracks'}), name='playlist-tracks'),
    path('api/user/', CustomUserAPIView.as_view(), name='user-detail'),
    path('api/genres/', GenreAPIView.as_view(), name='genres-list'),
    path('api/create_musician/', MusicianProfileAPIView.as_view(), name='create_musician'),

    path('api/posts/', PostsAPIView.as_view()),
    path('api/posts/<int:pk>/', PostListDestroyAPIView.as_view()),
    path('api/musician_posts/<int:pk>/', MusicianPostsAPIView.as_view()),
    path('api/musician_posts/add_post/', NewMusicianPostAPIView.as_view()),
    path('api/musician_posts/add_post/<int:pk>/', ModifyMusicianPostAPIView.as_view()),
]

#urlpatterns += doc_urls
