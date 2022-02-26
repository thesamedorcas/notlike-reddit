from multiprocessing import context
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from .models import Tag, Conversation, Goal

# TODO move users to seperate app


def userLogin(request):
    toDisplay =  'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email =  request.POST.get('email').lower()
        password =  request.POST.get('password')

        try:
            print("testing auth")
        except:
            print("failed")
    return 'login'


def userRegister(request):
    pass


def userLogout(request):
    pass


def userProfile(request):
    pass


def userUpdate(request):
    pass


def home(request):
    print("home was hit")
    # TODO give user change to query
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
    return render(request, 'communities/home.html', context)


# TODO move goal to seperate app / rename tro communities
def getGoal(request):
    pass


def createGoal(request):
    pass


def updateGoal(request):
    pass


def deleteGoal(request):
    pass


def tags(request):
    pass


def activites(request):
    pass
