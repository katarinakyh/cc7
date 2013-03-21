from django import template
from apps.account.models import Association, MyProfile
from apps.group.models import Group


register = template.Library()

@register.inclusion_tag('account/association_list.html')
def list_associations():
    a = Association.objects.all()[:16]
    return {'association_list':a,}

@register.inclusion_tag('account/friend_list.html')
def list_friends():
    f = MyProfile.objects.all()
    return {'friend_list':f,}


def list_groups():
    a = Group.objects.all()[:16]
    return {'group_list':a,}

register.inclusion_tag('group/group_list.html')(list_groups)
