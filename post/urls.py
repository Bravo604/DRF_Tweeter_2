
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import TweetViewSet

router = DefaultRouter()
router.register('tweet', TweetViewSet, basename='tweet')
# router.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('tweet/<int:tweet_id>/comments/', views.CommentListCreateAPIView.as_view()),
    path('tweet/<int:tweet_id>/comments/<int:pk>/', views.CommentRetrieveDestroyUpdateAPIView.as_view()),
    path('tweet/<int:tweet_id>/like/', views.PostTweetLike.as_view()),
    path('tweet/<int:tweet_id>/dislike/', views.PostTweetDisLike.as_view()),
    path('tweet/<int:tweet_id>/comments/<int:pk>/like/', views.PostCommentLike.as_view()),
    path('tweet/<int:tweet_id>/comments/<int:pk>/dislike/', views.PostCommentDisLike.as_view()),

]
