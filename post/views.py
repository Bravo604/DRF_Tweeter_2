from django.db import IntegrityError
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from .serializers import TweetSerializer, CommentSerializer
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from .models import Tweet, Comment, LikeTweet, LikeComment, DislikeTweet, DislikeComment
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


# class CommentViewSet(ModelViewSet):
#     serializer_class = CommentSerializer
#     queryset = Comment.objects.all()
#     authentication_classes = [SessionAuthentication, TokenAuthentication, ]
#     permission_classes = [IsAuthorPermission, ]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


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
    def get(self, request, tweet_id):
        tweet = get_object_or_404(Tweet, id=tweet_id)
        try:
            like = LikeTweet.objects.create(tweet=tweet, user=request.user)

        except IntegrityError:
            LikeTweet.objects.get(tweet=tweet, user=request.user).delete()
            data = {
                'message': f'{request.user.username} take back his like from tweet {tweet_id} '
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'message': f'tweet {tweet_id} got like from {request.user.username}'
            }
            return Response(data, status=status.HTTP_201_CREATED)


class PostTweetDisLike(APIView):
    def get(self, request, tweet_id):
        tweet = get_object_or_404(Tweet, id=tweet_id)
        try:
            dislike = DislikeTweet.objects.create(tweet=tweet, user=request.user)

        except IntegrityError:
            DislikeTweet.objects.get(tweet=tweet, user=request.user).delete()
            data = {
                'message': f'{request.user.username} take back his dislike from tweet {tweet_id} '
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'message': f'tweet {tweet_id} got dislike from {request.user.username}'
            }
            return Response(data, status=status.HTTP_201_CREATED)


class PostCommentLike(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer

    def get(self, request, tweet_id, pk):
        comment = get_object_or_404(Comment, id=tweet_id, pk=pk)
        try:
            like = LikeComment.objects.create(comment=comment, user=request.user)

        except IntegrityError:
            LikeComment.objects.get(comment=comment, user=request.user).delete()
            data = {
                'message': f'{request.user.username} take back his like from comment {pk} '
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'message': f'comment {pk} got like from {request.user.username}'
            }
            return Response(data, status=status.HTTP_201_CREATED)


class PostCommentDisLike(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer

    def get(self, request, tweet_id, pk):
        comment = get_object_or_404(Comment, id=tweet_id, pk=pk)
        try:
            dislike = DislikeComment.objects.create(comment=comment, user=request.user)

        except IntegrityError:
            DislikeComment.objects.get(comment=comment, user=request.user).delete()
            data = {
                'message': f'{request.user.username} take back his dislike from comment {pk} '
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'message': f'comment {pk} got dislike from {request.user.username}'
            }
            return Response(data, status=status.HTTP_201_CREATED)