from django.contrib import admin

from .models import CustomUser, MusicianProfile, Subscription

admin.site.register(CustomUser)
admin.site.register(MusicianProfile)
admin.site.register(Subscription)
