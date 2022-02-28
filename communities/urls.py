from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name="home"),
    path('auth', views.userLogin, name="login"),
    path('auth/register', views.userRegister, name="register"),
    path('auth/logout', views.userLogout, name="logout"),
    path('profile/<str:id>/', views.Profile, name="profile"),
    path('update-profile' , views.userUpdate , name="update-user"),

    path('topics' , views.tags , name = "topics"),
    path('recent' ,  views.recent,  name="recent"),

    path('goal<str:id>/' , views.getGoal ,  name="goal")
]
