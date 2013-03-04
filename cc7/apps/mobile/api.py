# post/api.py
from django.contrib.auth.models import User
from userena.models import UserenaBaseProfile, upload_to_mugshot
from tastypie import fields
from tastypie.resources import ModelResource
from apps.publication.models import Post, Comment
from apps.event.models import Event
from apps.account.models import MyProfile, Association
from django.forms.models import model_to_dict


class UserResource(ModelResource):
    class Meta:
        queryset= User.objects.all()
        include_resource_uri = False
        excludes = 'password, is_staff, is_superuser'
    


class AuthorResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)

    class Meta:
        queryset= MyProfile.objects.all()
        include_resource_uri = False

class EventResource(ModelResource):
    class Meta:
        queryset= Event.objects.all()
        include_resource_uri = False

class PostResource(ModelResource):
    author = fields.ToOneField(AuthorResource, 'author', full=True)
        
    class Meta:
        queryset = Post.objects.all().order_by('-date_created')
        resource_name = 'post'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']        
    
    def dehydrate(self, bundle):
        user = MyProfile.objects.get(pk = bundle.obj.author.pk)
        mugshot = user.get_mugshot_url()
        bundle.data['mugshot'] = mugshot
        
        comments = Comment.objects.filter(post = bundle.obj.pk)
        bundle.data['comment_count'] = len(comments)
        bundle.data['comments'] = [model_to_dict(c) for c in comments]
        return bundle
    
class CommentResource(ModelResource):
    author = fields.ToOneField(AuthorResource, 'author', full=True)
    post = fields.ToOneField(PostResource, 'post', full=True)
    event = fields.ToOneField(EventResource, 'event', full=True)
    
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'put']        
