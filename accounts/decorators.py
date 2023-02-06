from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect, HttpResponse, Http404


def guest_user(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse("Already logged in. Please log out to login again.")
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def login_user(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from utils.Constants import LOGIN_URL
            return redirect(LOGIN_URL)
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def admin_user(function):
    def wrap(request, *args, **kwargs):
        from utils.Constants import UserRoleChoice
        if request.user.is_authenticated and request.user.role == UserRoleChoice.Admin.value:
            return function(request, *args, **kwargs)
        else:
            from utils.Constants import LOGIN_URL
            return HttpResponse("You are not a Admin")
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

