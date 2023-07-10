from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from music.views import PlaylistViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('playlists', PlaylistViewSet, basename='playlist')

urlpatterns = router.urls

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/register/', include('djoser.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('api/', include(router.urls)),
    path('api/playlists/<int:pk>/add_track/<int:track_id>/', PlaylistViewSet.as_view({'post': 'add_track'}), name='playlist-add-track'),
    path('api/playlists/<int:pk>/tracks/', PlaylistViewSet.as_view({'get': 'tracks'}), name='playlist-tracks')
]
