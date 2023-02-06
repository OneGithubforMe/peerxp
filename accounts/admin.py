from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
from .forms import UserAdminCreationForm, UserAdminChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import profile_information


User = get_user_model()

class UserAdmin(BaseUserAdmin):
    # The form to change user instenses
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # the fields to be used in displaying the user model
    # these override the definitation on the base Usermodel
    # that refresnce specific fields on auth.user
    list_display = ('name', 'email', 'country_code', 'phone_number', 'role', 'department', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('name', 'email', 'country_code', 'phone_number', 'password','role', 'department')}),
        # ('Personal info', {'fields' : ()}),
        ('Permissions', {'fields': ('is_superuser', 'groups', 'user_permissions')})
    )

    # add_fieldsets is not a standard Model admin attribute. UserAdmin
    # overrides get_fieldset to use this attribute when creating a user.

    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('name', 'email', 'country_code', 'phone_number', 'password', 'role', 'department')
        }),
    )

    search_fields = ('email', 'phone_number', 'name',)
    ordering = ()
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(User, UserAdmin)


