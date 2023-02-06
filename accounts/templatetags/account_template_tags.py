from django import template
register = template.Library()

@register.simple_tag
def is_admin(role):
    from utils.Constants import UserRoleChoice
    return role == UserRoleChoice.Admin.value
