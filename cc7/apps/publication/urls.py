from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from apps.publication.views import PostView, AddPostView, AddMessageView, delete_comment
from apps.stream.views import stream, stream_posts


urlpatterns = patterns('',
    url(r'^list/$', login_required(PostView.as_view()), name= 'list_posts'),
    url(r'^add/$', login_required(AddPostView.as_view()), name= 'add_post'),
    url(r'^detail/(?P<pk>[-_\w]+)/$', 'apps.publication.views.post_detail', name='postdetailview'),
    url(r'^message/$', login_required(AddMessageView.as_view()), name= 'add_message'),
    url(r'^filter/$', login_required(stream_posts), name= 'stream_posts'),
    url(r'^edit/(?P<type>[-_\w]+)/(?P<pk>[-_\w]+)$', login_required(stream_posts), name= 'stream_posts'),
    url(r'^delete/comment/(?P<pk>[a-zA-Z0-9_.-]+)/$', login_required(delete_comment), name= 'delete_comment'),

)