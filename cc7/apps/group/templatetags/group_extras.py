from django import template
from django.templatetags.static import register
from apps.group.models import Group

register = template.Library()

def list_groups():
    a = Group.objects.all()[:16]
    return {'group_list':a,}

register.inclusion_tag('group/group_list.html')(list_groups)
