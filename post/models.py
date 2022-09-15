from django.db import models
from django.db.models.signals import pre_save, post_save
from django.db.models import Count

from account.models import User


class Post(models.Model):
    text = models.CharField(max_length=140)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.__class__.__name__} from {self.user.username} at {self.updated}'

    @property
    def post_username(self):
        return self.user.username


class Tweet(Post):
    text = models.CharField(max_length=140)

    def get_status(self):
        like_dislike = LikeDislikeTweet.objects.filter(tweet=self).values('status__status_name'). \
            annotate(count=Count('status'))
        statuses = {}
        for i in like_dislike:
            statuses[i['status__status_name']] = i['count']
        return statuses


class Comment(Post):
    text = models.CharField(max_length=255)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    def get_status(self):
        like_dislike = LikeDislikeComment.objects.filter(comment=self).values('status__status_name'). \
            annotate(count=Count('status'))
        statuses = {}
        for i in like_dislike:
            statuses[i['status__status_name']] = i['count']
        return statuses


class TweetStatus(models.Model):
    slug = models.CharField(max_length=20, unique=True)
    status_name = models.CharField(max_length=20)

    def __str__(self):
        return self.status_name


class LikeDislikeTweet(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(TweetStatus, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tweet')

    def __str__(self):
        return f'{self.tweet} - {self.user.username} - {self.status.status_name}'


class LikeDislikeComment(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(TweetStatus, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tweet')

    def __str__(self):
        return f'{self.tweet} - {self.comment} - {self.user.username} - {self.status.status_name}'

