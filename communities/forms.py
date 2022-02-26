import profile
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import userProfile, Goal
from django.contrib.auth.models import User


class newUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'
        #['name', 'username', 'email', 'password1', 'password2']
        # TODO exclude is there is role


class userProfileForm(ModelForm):
    class Meta:
        model = userProfile
        fields = '__all__'
        exclude = ['user']



class goalForm():
    class Meta:
        model = Goal
        fields = '__all__'
        exclude = ['created_by', 'members']
