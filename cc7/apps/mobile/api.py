# post/api.py
from django.contrib.auth.models import User
from userena.models import UserenaBaseProfile, upload_to_mugshot
from tastypie import fields
from tastypie.resources import ModelResource
from apps.publication.models import Post
from apps.account.models import MyProfile, Association



class UserResource(ModelResource):
    #mugshot = fields.CharField(get_mugshot_url(self))
    class Meta:
        queryset= User.objects.all()
        #mugshot = get_mugshot_url(self)
        include_resource_uri = False
        excludes = 'password, is_staff, is_superuser'
    


class AuthorResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)

    class Meta:
        queryset= MyProfile.objects.all()
        include_resource_uri = False


class PostResource(ModelResource):
    author = fields.ToOneField(AuthorResource, 'author', full=True)
    
    class Meta:
        queryset = Post.objects.all().order_by('-date_created')
        resource_name = 'post'
        list_allowed_methods = ['get']
        
    
    def dehydrate(self, bundle):
        user = MyProfile.objects.get(pk = bundle.obj.author.pk)
        mugshot = user.get_mugshot_url()
        bundle.data['mugshot'] = mugshot
        return bundle