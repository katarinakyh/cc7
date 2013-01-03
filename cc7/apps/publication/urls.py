from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from apps.publication.views import PostView, AddPostView


urlpatterns = patterns('',
    url(r'^list/$', login_required(PostView.as_view()), name= 'list_posts'),
    url(r'^add/$', login_required(AddPostView.as_view()), name= 'add_post'),
    url(r'^detail/(?P<pk>[-_\w]+)/$', 'apps.publication.views.post_detail', name='postdetailview'),
)