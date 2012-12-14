from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from apps.publication.views import PostView, AddPostView


urlpatterns = patterns('cc7.apps.event.views',
    url(r'^list/$', login_required(PostView.as_view()), name= 'list_posts'),
    url(r'^add/$', login_required(AddPostView.as_view()), name= 'add_post'),
)