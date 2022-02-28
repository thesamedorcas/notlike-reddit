from multiprocessing import context
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Q
from .models import Tag, Conversation, Goal, userProfile
from django.contrib.auth import authenticate, login, logout
from .forms import newUserCreationForm, userProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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
    context = {'toDisplay': toDisplay}
    return render(request, 'communities/auth.html', context)


def userRegister(request):
    form = newUserCreationForm()
    if request.method == 'POST':
        try:
            isValid = newUserCreationForm(request.POST).is_valid()
            if isValid == True:
                user = newUserCreationForm(request.POST).save(commit=False)
                user.username = user.username.lower()
                user.save()
                userProfile.objects.create(user=user)
                login(request, user)
                return redirect('home')
        except:
            messages.error(
                request, '😕 .something went wrong with registration .')
    context = {'form': form}
    return render(request, 'communities/auth.html', context)


def userLogout(request):
    logout(request)
    return redirect('home')


def Profile(request, id):
    try:
        user = User.objects.get(username=id)
        profile = user.userprofile
        goals = user.goal_set.all()
        conversations = user.conversation_set.all()
        tags = Tag.objects.all()
        context = {'user': user, 'profile': profile, 'goals': goals,
                   'conversations': conversations, 'tags': tags}
        return render(request, 'communities/user_profile.html', context)
    except:
        messages.error(request, '😕 .User does not exist .')
        # TODO home ||  profile with message
        return HttpResponse("failure")


# TODO add LOGIN_URL in settings.py later
@login_required(login_url='/auth')
def userUpdate(request):
    user = request.user
    userForm = newUserCreationForm(instance=user)
    profileForm = userProfileForm(instance=user.userprofile)
    context = {'userform': userForm, 'profileform': profileForm}
    if request.method == 'POST':
        userForm = newUserCreationForm(request.POST, instance=user)
        profileForm = userProfileForm(
            request.POST, request.FILES, instance=user.userprofile)
        if userForm.is_valid():
            userForm.save()
            context['userform'] = userForm
        if profileForm.is_valid():
            profileForm.save()
            context['profileform'] = profileForm
        return redirect(to='profile', id = user.username)
    return render(request, 'communities/update_user.html', context)


def home(request):
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
