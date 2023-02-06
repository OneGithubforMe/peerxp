from django import forms
from django.forms import BaseFormSet
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import *
from django.forms import ModelForm


class UserAdminCreationForm(forms.ModelForm):
    # form for creating new users. Include all required fields
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    name = forms.CharField(label='Your Name', widget=forms.TextInput)

    class Meta:
        model = get_user_model()
        fields = ('name', 'email')

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        # save the provided password in hashed Format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    # A form for updating sers.

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = get_user_model()
        fields = ('name', 'email', 'password', 'is_superuser')

    def clean_password(self):
        # regardless of what the user provides, return the initial value
        # this is done here, rather then on the field, because the
        # field does not have access to the initial value
        return self.initial['password']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())


from django.contrib.auth.forms import UserCreationForm
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'phone_number', 'department', 'role')


class UserUpdateDepartmentModelForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('department',)
