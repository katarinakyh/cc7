from django.conf.urls import url,  include, patterns
from django.contrib.auth.decorators import login_required
from views import PostsView
from api import PostResource, CommentResource, AuthorResource, PlaceResource
from tastypie.api import Api

v1 = Api('v1')
v1.register(PostResource())
v1.register(CommentResource())
v1.register(AuthorResource())
v1.register(PlaceResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1.urls)),
    url(r'^$', login_required(PostsView.as_view()), name='PostsView'),
)

