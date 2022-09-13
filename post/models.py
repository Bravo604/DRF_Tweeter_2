from django.db import models

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

    def get_likes(self):
        likes = LikeTweet.objects.filter(tweet=self)
        return likes.count()

    def get_dislikes(self):
        dislikes = DislikeTweet.objects.filter(tweet=self)
        return dislikes.count()


class Comment(Post):
    text = models.CharField(max_length=255)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)

    def get_likes(self):
        likes = LikeComment.objects.filter(comment=self)
        return likes.count()

    def get_dislikes(self):
        dislikes = DislikeComment.objects.filter(comment=self)
        return dislikes.count()


class LikeTweet(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tweet')
# не разобрался как изменить
    # def save(self, *args, **kwargs):
    #     if DislikeTweet(id=self.tweet_id) == True:
    #         DislikeTweet(id=self.tweet_id).delete()
    #         super().save(*args, **kwargs)


class DislikeTweet(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'tweet',)

    # def save(self, *args, **kwargs):
    #     if LikeTweet(id=self.tweet_id):
    #         LikeTweet(id=self.tweet_id).delete()
    #         super().save(*args, **kwargs)


class LikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'comment')

        # def save(self, *args, **kwargs):
        #     if DislikeTweet(id=self.comment_id):
        #         LikeTweet(id=self.comment_id).delete()
        #         super().save(*args, **kwargs)


class DislikeComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'comment')

        # def save(self, *args, **kwargs):
        # if LikeComment(id=self.comment_id):
        #     LikeComment(id=self.comment_id).delete()
        #     super().save(*args, **kwargs)

