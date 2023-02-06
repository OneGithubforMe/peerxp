
def check_data_and_login_user(request, form):
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

    return True, "Login successful."


def check_data_and_save_user(request, form):
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
        return True, "User created successful."
    else:
        return False, "Please correct the data."
