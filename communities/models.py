from django.db import models
from sqlalchemy import true
from django.contrib.auth.models import User

# Create your models here.


class userProfile(models.Model):
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(null=true)
    created = models.DateTimeField(auto_now_add=true)
    avatar = models.ImageField(upload_to='avatars', default='avatar.svg')

    def __str__(self):
        return str(self.user.username)


class Tag(models.Model):

    name = models.CharField(max_length=50)
    # isfollowing

    def __str__(self):
        return self.name


class Goal(models.Model):
    created_by = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True)
    members = models.ManyToManyField(
        to=User, related_name='members', blank=true)
    tag = models.ForeignKey(to=Tag, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    updated = models.DateTimeField(auto_now=true)
    created = models.DateTimeField(auto_now_add=true)

    def __str__(self):
        return self.name
    # conversation

    class Meta:
        ordering = ["-updated", "-created"]


class Conversation(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True)
    goal = models.ForeignKey(to=Goal, on_delete=models.CASCADE)
    body = models.TextField(max_length=200)
    updated = models.DateTimeField(auto_now=true)
    created = models.DateTimeField(auto_now_add=true)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.body[0:20]
