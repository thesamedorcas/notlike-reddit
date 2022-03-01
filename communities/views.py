from multiprocessing import context
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.db.models import Q
from .models import Tag, Conversation, Goal, userProfile
from django.contrib.auth import authenticate, login, logout
from .forms import newUserCreationForm, userProfileForm, goalForm
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
        return redirect(to='profile', id=user.username)
    return render(request, 'communities/update_user.html', context)


def home(request):
    query = request.GET.get('query') if request.GET.get(
        'query') != None else ''
    # TODO limitt return in each query
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
def getGoal(request, id):
    msg = "getting goal with id " + id
    goal = Goal.objects.get(id=id)
    conversations = goal.conversation_set.all()
    members = goal.members.all()
    context = {'goal': goal,
               'conversations': conversations, 'members': members}
    return render(request, 'communities/goal.html', context)


@login_required(login_url='/auth')
def createGoal(request):
    form = goalForm()
    tags = Tag.objects.all()
    try:
        if request.method == "POST":
            usertag = request.POST.get('tag')
            tag, created = Tag.objects.get_or_create(name=usertag)
            Goal.objects.create(
                created_by=request.user,
                name=request.POST.get('name'),
                tag=tag,
                description=request.POST.get('description')
            )
            return redirect('home')
    except:
        messages.error(request, "goal not created")
    context = {'form': form, 'tags': tags}
    return render(request, 'communities/goal_form.html', context)


@login_required(login_url='/auth')
def updateGoal(request, id):
    tags = Tag.objects.all()
    context = {"tags": tags}
    try:
        goal = Goal.objects.get(id=id)
        if goal.created_by == request.user:
            if request.method == 'POST':
                usertag = request.POST.get('tag')
                tag, created = Tag.objects.get_or_create(name=usertag)
                goal.objects.update(tag=tag, name=request.POST.get(
                    'name'), description=request.POST.get("description"))
                return redirect('home')
            context['data'] = {'name': goal.name,
                               'description': goal.description, 'current_tag': goal.tag}
            return render(request, 'communities/goal_form.html', context)
        else:
            raise Exception('no permisson')
    except:
        messages.error(request, "You cannot make changes to this")
        return redirect('home')


@login_required(login_url='/auth')
def deleteGoal(request, id):
    try:
        goal = Goal.objects.get(id=id)
        if goal.created_by == request.user:
            if request.method == 'POST':
                goal.delete()
                return redirect('home')
            return render(request, 'communities/delete.html', {'obj': goal})
        else:
            raise Exception('no permisson')
    except:
        messages.error(request, "You cannot delete this")
        return redirect('home')


def tags(request):
    query = request.GET.get('query') if request.GET.get(
        'query') != None else ''
    tags = Tag.objects.filter(name__icontains=query)
    context = {'tags': tags}
    return render(request, 'communities/tags.html', context)


def recent(request):
    conversations = Conversation.objects.all()[0:20]
    return render(request, 'communities/recent.html', {'conversations':  conversations})
