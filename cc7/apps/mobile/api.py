# post/api.py
from django.contrib.auth.models import User
from userena.models import UserenaBaseProfile, upload_to_mugshot
from tastypie import fields
from tastypie.paginator import Paginator
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authorization import Authorization
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from apps.publication.models import Post, Comment
from apps.event.models import Event
from apps.account.models import MyProfile, Association
from django.forms.models import model_to_dict
from apps.map.models import Place
from haystack.query import SearchQuerySet

from django.http import Http404
from tastypie.utils import trailing_slash
from django.conf.urls.defaults import *

class UserResource(ModelResource):
    class Meta:
        queryset= User.objects.all()
        include_resource_uri = False
        excludes = 'password, is_staff, is_superuser, last_login, date_joined, email, is_active, last_name'
        allowed_methods = ['get']
        filtering = {
            'user' : ALL_WITH_RELATIONS,
            'pk': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        authorization= Authorization()

class AuthorResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)

    class Meta:
        queryset= MyProfile.objects.all()
        include_resource_uri = False
        excludes = 'password, is_staff, is_superuser, last_login, date_joined, email, is_active, last_name'
        allowed_methods = ['get','post']
        filtering = {
            'profile' : ALL_WITH_RELATIONS,
            'pk': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        authorization= Authorization()

class EventResource(ModelResource):
    class Meta:
        queryset= Event.objects.all()
        include_resource_uri = False

class PlaceResource(ModelResource):
    class Meta:
        queryset = Place.objects.all()
        allowed_methods = ['get', 'post', 'put']
        authorization= Authorization()
        filtering = {
            'profile' : ALL_WITH_RELATIONS,
            'pk': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        always_return_data = True

class PostResource(ModelResource):
    author = fields.ToOneField(AuthorResource, 'author', full=True)
    place = fields.ToOneField(PlaceResource, 'place', full=True, null=True)
    event = fields.ToOneField(EventResource, 'event', full=True, null=True)

    class Meta:
        queryset = Post.objects.filter(is_public=True).order_by('-date_created')
        resource_name = 'post'
        list_allowed_methods = ['get', 'post']
        paginator_class = Paginator
        allowed_methods = ['get', 'post']
        filtering = {
            'body': ALL,
            'author' : ALL_WITH_RELATIONS,
            'id': ['exact', 'range', 'gt', 'gte', 'lt', 'lte'],
        }
        always_return_data = True
        # insecure!: must be change to methods below when done testing
        authorization= Authorization()


    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
            ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        sqs = SearchQuerySet().models(Post).load_all().auto_query(request.GET.get('q', ''))
        print sqs
        objects = []

        for result in sqs:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
            }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)

    def dehydrate(self, bundle):
        user = MyProfile.objects.get(pk = bundle.obj.author.pk)
        mugshot = user.get_mugshot_url()
        bundle.data['mugshot'] = mugshot

        bundle.data['date_created'] =  bundle.obj.date_created.strftime("%A %d %B %Y at %H:%M")
        
        comments = Comment.objects.filter(post = bundle.obj.pk)
        i = 0
        commentsdict  = {  }
        for c in comments:
            commentsdict[i] = {  }
            commentsdict[i]['comment_id'] = c.id
            commentsdict[i]['comment_date'] = c.date_created.strftime("%A %d %B %Y at %H:%M")
            commentsdict[i]['comment_body'] = c.body
            commentsdict[i]['author'] = c.author
            commentsdict[i]['author_id'] = c.author.id
            commentsdict[i]['author_name'] = c.author.user
            commentsdict[i]['author_mugshot'] = c.author.get_mugshot_url()
            i = i + 1


        bundle.data['comment_count'] = len(comments)
        bundle.data['comments'] = commentsdict
        return bundle

class CommentResource(ModelResource):
    author = fields.ToOneField(AuthorResource, 'author', full=True)
    post = fields.ToOneField(PostResource, 'post', full=True)
    event = fields.ToOneField(EventResource, 'event', full=True)

    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
        allowed_methods = ['get', 'post']
        # insecure!: must be change to methods below when done testing
        authorization= Authorization()
        #authentication = BasicAuthentication()
        #authorization = DjangoAuthorization()