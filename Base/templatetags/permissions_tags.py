from django import template #type:ignore

register = template.Library()

@register.filter
def is_admin(user):
    return user.is_superuser
