from django.db import models
from user.models import User
from django.utils.timesince import timesince


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    post_text = models.TextField(max_length=350)
    post_image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, through='PostLike', related_name='likes', blank=True, null=True)
    comments = models.ManyToManyField(User,
                                      through='PostComment', related_name='comments', blank=True, null=True)

    def format_timesince(self):
        return timesince(self.created_at)

    def __str__(self):
        return f"Post by {self.creator.username}"


class postcommon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class PostLike(postcommon):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

    class Meta:
        unique_together = ('user', 'post')


class PostComment(postcommon):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    comment = models.TextField(max_length=300)

    def __str__(self):
        return f"{self.comment[:30]}... by {self.user.username}"
