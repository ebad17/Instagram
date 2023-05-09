from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.contrib.auth.models import User


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_friend')

    def __str__(self):
        return str(self.friend)

    class Meta:
        unique_together = ('user', 'friend')


class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    message = models.TextField()
    content = models.FileField(upload_to='data/story')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} {self.created_at}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_likes', null=True, blank=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='story_likes', null=True, blank=True)

    def __str__(self):
        return str(self.user)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', null=True, blank=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=255)
    reply = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name='user_reply')

    def __str__(self):
        return f"{self.user} {self.comment} {self.reply}"
