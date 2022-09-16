from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from .serializers import TweetSerializer, CommentSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .models import Tweet, Comment, LikeDislikeTweet, LikeDislikeComment, TweetStatus
from .permissions import IsAuthorPermission
from .paginations import StandardPagination


class TweetViewSet(ModelViewSet):
    serializer_class = TweetSerializer
    queryset = Tweet.objects.all()
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthorPermission, ]
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user__username=user)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(text__icontains=search)
        return queryset


class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthorPermission, ]
    pagination_class = StandardPagination

    def get_queryset(self):
        return self.queryset.filter(tweet_id=self.kwargs['tweet_id'])

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            tweet=get_object_or_404(Tweet, id=self.kwargs['tweet_id'])
        )


class CommentRetrieveDestroyUpdateAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication, ]
    permission_classes = [IsAuthorPermission, ]


class PostTweetLike(APIView):
    def get(self, request, tweet_id, status_slug):
        tweet = get_object_or_404(Tweet, id=tweet_id)
        tweet_status = get_object_or_404(TweetStatus, slug=status_slug)
        try:
            like_dislike = LikeDislikeTweet.objects.create(tweet=tweet, user=request.user, status=tweet_status)
        except IntegrityError:
            like_dislike = LikeDislikeTweet.objects.get(tweet=tweet, user=request.user)
            if like_dislike.status == tweet_status:
                like_dislike.status = None
            else:
                like_dislike.status = tweet_status
            like_dislike.save()
            data = {
                'message': f'{tweet_id} changed status by {request.user.username}'
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'message': f'tweet {tweet_id} got status from {request.user.username}'
            }
            return Response(data, status=status.HTTP_201_CREATED)


class PostCommentLikeDislike(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer

    def get(self, request, tweet_id, pk, status_slug):
        comment = get_object_or_404(Comment, id=tweet_id, pk=pk)
        tweet_status = get_object_or_404(TweetStatus, slug=status_slug)
        try:
            like_dislike = LikeDislikeComment.objects.create(comment=comment, user=request.user, status=tweet_status)
        except IntegrityError:
            like_dislike = LikeDislikeTweet.objects.get(comment=comment, user=request.user,)
            like_dislike.status = tweet_status
            like_dislike.save()
            data = {
                'message': f'{pk} to {tweet_id} changed status by {request.user.username}'
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'message': f'comment {pk} to tweet {tweet_id} got status from {request.user.username}'
            }
            return Response(data, status=status.HTTP_201_CREATED)




