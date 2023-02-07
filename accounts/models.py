from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from utils.Constants import DEFAULT_COUNTRY_CODE


class UserManager(BaseUserManager):
    def create_user(self, username, name, email=None, country_code=None, phone_number=None, password=None, staff=False, admin=False, **extra_fields):
        if not username:
            raise ValueError("user must have a username")
        from utils.Functions import check_if_valid_email
        if check_if_valid_email(username):
            email = username
        else:
            from utils.Functions import get_valid_phone_number
            phone_number = get_valid_phone_number(username)

        if not password:
            raise ValueError("user must have a password")
        if not name:
            raise ValueError("User must have a name")
        if not country_code:
            country_code = DEFAULT_COUNTRY_CODE
        user_obj = self.model(
            username=username,
            name=name,
            email=self.normalize_email(email),
            phone_number=phone_number,
            **extra_fields
        )

        user_obj.username = email if email else f'{country_code}{phone_number}'
        user_obj.set_password(password)  # change user password
        user_obj.is_staff = staff
        user_obj.is_superuser = admin
        if admin:
            user_obj.role = UserRoleChoice.Admin.value
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, username, name, email=None, phone_number=None, password=None, **extra_fields):
        user = self.create_user(
            username,
            name,
            email,
            phone_number,
            password=password,
            staff=True, **extra_fields
        )
        return user

    def create_superuser(self, username, name, email=None, phone_number=None, password=None, **extra_fields):
        user = self.create_user(
            username,
            name,
            email,
            phone_number,
            password=password,
            staff=True,
            admin=True, **extra_fields
        )
        return user


from department.models import Department
from utils.Constants import UserRoleChoice, USER_ROLE_CHOICE


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, primary_key=True)
    name = models.CharField(verbose_name='Full name', max_length=255)
    email = models.EmailField(verbose_name='email', max_length=255, unique=True, null=True, blank=True)
    country_code = models.CharField(max_length=10, default=DEFAULT_COUNTRY_CODE)
    phone_number = models.CharField(verbose_name='phone number', max_length=20, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True)
    role = models.PositiveIntegerField(choices=USER_ROLE_CHOICE, default=UserRoleChoice.User.value)
    is_staff = models.BooleanField(default=False)
    created_by = models.ForeignKey('accounts.user', on_delete=models.PROTECT, blank=True, null=True, verbose_name='Created by')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', ]

    objects = UserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['country_code', 'phone_number'], name='unique_phone_country_code')
        ]

    def __str__(self):
        return self.email if self.email else self.phone_number

    def get_name(self):
        return self.name