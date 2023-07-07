from django.contrib import admin

from .models import CustomUser, MusicianProfile

admin.site.register(CustomUser)
admin.site.register(MusicianProfile)
