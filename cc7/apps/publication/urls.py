from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from apps.publication.views import PostView, AddPostView, PostDetailView, AddMessageView


urlpatterns = patterns('cc7.apps.post.views',
    url(r'^list/$', login_required(PostView.as_view()), name= 'list_posts'),
    url(r'^add/$', login_required(AddPostView.as_view()), name= 'add_post'),
    url(r'^message/$', login_required(AddMessageView.as_view()), name= 'add_message'),
    url(r'^detail/(?P<pk>[-_\w]+)/$', login_required(PostDetailView.as_view()), name='postdetailview'),
)