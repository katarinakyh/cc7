from tastypie.resources import ModelResource
from django.contrib.auth.models import User
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from models import Group, ActiveMember
from apps.account.models import MyProfile


class UserResource(ModelResource):
    class Meta:
        queryset= User.objects.all()
        resource_name = 'user'
        include_resource_uri = False
        excludes = 'password, is_staff, is_superuser, last_login, date_joined, email, is_active, last_name'
        allowed_methods = ['get']
        authorization = DjangoAuthorization()

class MyprofileResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)

    class Meta:
        queryset= MyProfile.objects.all()
        resource_name = 'myprofile'
        include_resource_uri = False
        excludes = 'password, is_staff, is_superuser, last_login, date_joined, email, is_active, last_name'
        allowed_methods = ['get','post']
        authorization = DjangoAuthorization()

class GroupResource(ModelResource):
    class Meta:
        queryset = Group.objects.all()
        resource_name = 'group'
        allowed_methods = ['get']
        always_return_data = True
        authorization = DjangoAuthorization()

class ActiveMemberResource(ModelResource):
    member = fields.ToOneField(MyprofileResource, 'member', full=True)
    group = fields.ForeignKey(GroupResource, 'group', full=True)

    class Meta:
        queryset = ActiveMember.objects.all()
        resource_name = 'active_members'
        allowed_methods = ['get', 'post', 'put']
        always_return_data = True
        authorization = DjangoAuthorization()


