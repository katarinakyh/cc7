from django.conf.urls import url, patterns
from apps.publication.views import PostView, AddPostView


urlpatterns = patterns('cc7.apps.event.views',
    url(r'^list/$', PostView.as_view(), name= 'list_posts'),
    url(r'^add/$', AddPostView.as_view(), name= 'add_post'),
)