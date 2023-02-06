from django.contrib import admin
from django.urls import path, include
from .views import UserLogin, CreateUser, logout_user#, UsersListView

app_name="accounts"

urlpatterns = [
    path('login', UserLogin.as_view(), name="user-login"),
    path("logout", logout_user, name="user-logout"),
    # path('user/', UsersListView.as_view(), name="user-create"),
    path('user/create', CreateUser.as_view(), name="user-create"),
    # path('', include('django.contrib.auth.urls')),
]