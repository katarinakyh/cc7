# post/api.py
from django.contrib.auth.models import User
from userena.models import UserenaBaseProfile, upload_to_mugshot
from tastypie import fields
from tastypie.paginator import Paginator
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from apps.publication.models import Post, Comment
from apps.event.models import Event
from apps.account.models import MyProfile, Association
from django.forms.models import model_to_dict


class UserResource(ModelResource):
    class Meta:
        queryset= User.objects.all()
        include_resource_uri = False
        excludes = 'password, is_staff, is_superuser, last_login, date_joined, email, is_active, last_name'
        allowed_methods = ['get']



class AuthorResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user', full=True)

    class Meta:
        queryset= MyProfile.objects.all()
        include_resource_uri = False
        excludes = 'password, is_staff, is_superuser, last_login, date_joined, email, is_active, last_name'
        allowed_methods = ['get']


class EventResource(ModelResource):
    class Meta:
        queryset= Event.objects.all()
        include_resource_uri = False

class PageNumberPaginator(Paginator):
    def page(self):
        output = super(PageNumberPaginator, self).page()
        output['page_number'] = int(self.offset / self.limit) + 1
        return output
    
class PostResource(ModelResource):
    author = fields.ToOneField(AuthorResource, 'author', full=True)

    class Meta:
        queryset = Post.objects.all().order_by('-date_created')
        resource_name = 'post'
        list_allowed_methods = ['get']
        paginator_class = Paginator
        allowed_methods = ['get']


    def dehydrate(self, bundle):
        user = MyProfile.objects.get(pk = bundle.obj.author.pk)
        mugshot = user.get_mugshot_url()
        bundle.data['mugshot'] = mugshot


        comments = Comment.objects.filter(post = bundle.obj.pk)
        for c in comments:
            c.mugshot = c.author.mugshot


        i = 0
        commentsdict  = {  }
        for c in comments:
            commentsdict[i] = {  }
            commentsdict[i]['comment_id'] = c.id
            commentsdict[i]['comment_date'] = c.date_created
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