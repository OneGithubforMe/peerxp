from django.shortcuts import render, redirect
from django.views import View
from accounts.decorators import guest_user, login_user, admin_user
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.shortcuts import redirect, HttpResponse, Http404
from .forms import UserUpdateDepartmentModelForm


@method_decorator(guest_user, name='dispatch')
class UserLogin(View):

    def get(self, request):
        from accounts.forms import LoginForm
        context = {
            "login_form": LoginForm()
        }

        return render(request, 'accounts/login.html', context)

    def post(self, request):
        from accounts.forms import LoginForm
        form = LoginForm(request.POST)

        if form.is_valid():
            is_successful, response = self.check_data_and_login_user(request, form)
            if is_successful:
                return redirect("/")
            else:
                messages.error(request, response)
        context = {
            "login_form": LoginForm()
        }
        return render(request, 'accounts/login.html', context)

    def check_data_and_login_user(self, request, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        if not password:
            return False, "Password is empty"

        from utils.Functions import check_if_valid_email
        if (not check_if_valid_email(username)) and (not username.startswith("+")):
            from utils.Constants import DEFAULT_COUNTRY_CODE
            username = f'{DEFAULT_COUNTRY_CODE}{username}'

        from django.contrib.auth.models import auth
        user = None
        if username:
            user = auth.authenticate(username=username, password=password)
        else:
            return False, "Please provided login creds."

        if not user:
            return False, "Phone number or email doesn't exist"
        auth.login(request, user)

        return True, "Loing successful."


def logout_user(request):
    logout(request)
    return redirect("accounts:user-login")


@method_decorator(admin_user, name='dispatch')
class CreateUser(View):

    def get(self, request):
        from accounts.forms import SignUpForm
        context = {
            "signup_form": SignUpForm()
        }

        return render(request, 'accounts/user_create.html', context)

    def post(self, request):
        from accounts.forms import SignUpForm
        form = SignUpForm(request.POST)

        is_successful, response = self.check_data_and_save_user(request, form)
        if is_successful:
            messages.success(request, response)
        else:
            messages.error(request, response)
        context = {
            "signup_form": SignUpForm()
        }
        return render(request, 'accounts/signup.html', context)

    def check_data_and_save_user(self, request, form):
        if form.is_valid():
            obj = form.save(commit=False)
            if obj.email:
                obj.phone_number = None
            elif obj.phone_number:
                import re
                obj.phone_number = re.sub('[^0-9]+', '', obj.phone_number)
            else:
                return False, "Phone number or email is empty"
            obj.username = obj.email if obj.email else f'{obj.country_code}{obj.phone_number}'
            obj.created_by_id = request.user.username
            obj.save()
            return True, "Loing successful."
        else:
            return False, "Please coorect"



@login_user
def index_page(request):
    return render(request, "accounts/index.html")