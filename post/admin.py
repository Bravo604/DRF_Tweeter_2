from django.contrib import admin
from .models import TweetStatus, LikeDislikeTweet, LikeDislikeComment

admin.site.register(TweetStatus)
admin.site.register(LikeDislikeTweet)
admin.site.register(LikeDislikeComment)
# Register your models here.
