from django import template
from apps.account.models import Association, MyProfile

register = template.Library()

@register.inclusion_tag('account/association_list.html')
def list_associations():
    a = Association.objects.all()[:16]
    return {'association_list':a,}

@register.inclusion_tag('account/friend_list.html')
def list_friends():
    f = MyProfile.objects.all()
    return {'friend_list':f,}