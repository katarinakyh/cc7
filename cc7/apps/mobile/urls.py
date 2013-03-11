from django.conf.urls import url,  include, patterns
from django.contrib.auth.decorators import login_required
from views import PostsView, AddPostView
from api import PostResource, CommentResource, AuthorResource, PlaceResource, EventResource, UserResource
from tastypie.api import Api

v1 = Api('v1')
v1.register(PostResource())
v1.register(CommentResource())
v1.register(AuthorResource())
v1.register(PlaceResource())
v1.register(EventResource())
v1.register(UserResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1.urls)),
    url(r'^$', login_required(PostsView.as_view()), name='PostsView'),
    url(r'^newpost', login_required(AddPostView.as_view()), name='AddPostView')
)

