# shelf/api.py
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from apps.publication.models import Post

class PostResource(ModelResource):
    class Meta:
        queryset = Post.objects.all().order_by('-date_created')
        resource_name = 'post'
        list_allowed_methods = ['get']