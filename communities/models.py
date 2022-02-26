from django.db import models
from sqlalchemy import true

# Create your models here.


class Tag(models.Model):

    name = models.CharField(max_length=50)
    # isfollowing

    def __str__(self):
        return self.name


class Goal(models.Model):
    # created_by user
    tag = models.ForeignKey(to=Tag, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    updated = models.DateTimeField(auto_now=true)
    created = models.DateTimeField(auto_now_add=true)

    def __str__(self):
        return self.name
    # conversation

    class Meta:
        ordering = ["-updated" , "-created"]


class Conversation(models.Model):
    # user
    goal = models.ForeignKey(to=Goal, on_delete=models.CASCADE)
    body = models.TextField(max_length=200)
    updated = models.DateTimeField(auto_now=true)
    created = models.DateTimeField(auto_now_add=true)

    class Meta:
        ordering = ["-updated" , "-created"]

    def __str__(self):
        return self.body[0:20]
