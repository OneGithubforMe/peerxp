from django.shortcuts import render, redirect
from accounts.decorators import guest_user, login_user, admin_user
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect


@guest_user
def user_login(request):
    from accounts.forms import LoginForm
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            from .functions import check_data_and_login_user
            is_successful, response = check_data_and_login_user(request, form)
            if is_successful:
                return redirect("/")
            else:
                messages.error(request, response)
    context = {
        "login_form": LoginForm()
    }
    return render(request, 'accounts/login.html', context)


@admin_user
def create_user(request):
    from accounts.forms import CreateUserForm
    if request.POST:
        form = CreateUserForm(request.POST)

        from .functions import check_data_and_save_user
        is_successful, response = check_data_and_save_user(request, form)
        if is_successful:
            messages.success(request, response)
        else:
            messages.error(request, response)
    context = {
        "signup_form": CreateUserForm()
    }
    return render(request, 'accounts/user_create.html', context)


@login_user
def logout_user(request):
    logout(request)
    return redirect("accounts:user-login")


@login_user
def index_page(request):
    return render(request, "accounts/index.html")
