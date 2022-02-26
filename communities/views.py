from multiprocessing import context
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.db.models import Q
from .models import Tag, Conversation, Goal


def home(request):
    print("home was hit")
    query = ''
    # TODO arrange tag by goals under it
    #      limitt return in each query
    tags = Tag.objects.all()[0:9]

    goals = Goal.objects.filter(
        Q(tag__name__icontains=query) | Q(
            name__icontains=query) | Q(description__icontains=query)
    )
    goals_count = goals.count()

    goal_conversations = Conversation.objects.filter(
        Q(goal__tag__name__icontains=query))

    context = {'tags': tags, 'goals': goals, 'goals_count': goals_count,
               'goal_conversations': goal_conversations}
    return render(request , 'communities/home.html' , context )
