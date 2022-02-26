from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('auth', views.userLogin, name="login"),
    path('auth/register', views.userRegister, name="register")
]
