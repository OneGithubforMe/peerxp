from django.contrib import admin
from django.urls import path, include
from .views import user_login, create_user, logout_user

app_name="accounts"

urlpatterns = [
    path('login', user_login, name="user-login"),
    path("logout", logout_user, name="user-logout"),
    path('user/create', create_user, name="user-create"),
]