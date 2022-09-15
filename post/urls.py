
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import TweetViewSet

router = DefaultRouter()
router.register('tweet', TweetViewSet, basename='tweet')


urlpatterns = [
    path('', include(router.urls)),
    path('tweet/<int:tweet_id>/comments/', views.CommentListCreateAPIView.as_view()),
    path('tweet/<int:tweet_id>/comments/<int:pk>/', views.CommentRetrieveDestroyUpdateAPIView.as_view()),
    path('tweet/<int:tweet_id>/<str:status_slug>/', views.PostTweetLike.as_view()),
    path('tweet/<int:tweet_id>/comments/<int:pk>/<str:status_slug>/', views.PostCommentLikeDislike.as_view()),
]
