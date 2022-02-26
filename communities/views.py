from multiprocessing import context
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Q
from .models import Tag, Conversation, Goal
from django.contrib.auth import authenticate, login
from .forms import newUserCreationForm
from django.contrib.auth.models import User
# TODO move users to seperate app


def userLogin(request):
    toDisplay = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        try:
            # TODO find work around for email Abstract user did not work
            username = request.POST.get('username').lower()
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        except:
            messages.error(request, '😕 .something went wrong')
    context = {'todisplay': toDisplay}
    return render(request, 'communities/auth.html', context)


def userRegister(request):
    form = newUserCreationForm()
    if request.method == 'POST':
        try:
            isValid = newUserCreationForm(request.POST).is_valid()
            if isValid == True:
                user = User.objects.create_user(request.POST)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect('home')
        except:
            messages.error(
                request, '😕 .something went wrong with registration .')
    context = {'form': form}
    return render(request, 'communities/auth.html',context)


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
