from django.contrib import admin
from .models import Post, CommentInPost, LikeInPost

admin.site.register(Post)
admin.site.register(CommentInPost)
admin.site.register(LikeInPost)
