from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from apps.publication.views import PostView, AddPostView, AddMessageView, delete_post, edit_post
=======
from apps.publication.views import PostView, AddPostView, AddMessageView, delete_comment, EditCommentView
>>>>>>> c89b346732716de05645305b62389a1a1688d43e
from apps.stream.views import stream, stream_posts


urlpatterns = patterns('',
    url(r'^list/$', login_required(PostView.as_view()), name= 'list_posts'),
    url(r'^add/$', login_required(AddPostView.as_view()), name= 'add_post'),
    url(r'^detail/(?P<pk>[-_\w]+)/$', 'apps.publication.views.post_detail', name='show_post'),
    url(r'^message/$', login_required(AddMessageView.as_view()), name= 'add_message'),
<<<<<<< HEAD
    url(r'^filter/$', login_required(stream_posts), name= 'stream_posts'),
    url(r'^edit/(?P<model>[a-zA-Z0-9_.-]+)/(?P<pk>[a-zA-Z0-9_.-]+)/$', login_required(edit_post), name= 'stream_posts'),
    url(r'^delete/(?P<model>[a-zA-Z0-9_.-]+)/(?P<pk>[a-zA-Z0-9_.-]+)/$', login_required(delete_post), name= 'delete_comment'),
=======
    url(r'^filter/$', login_required(stream_posts), name='stream_posts'),

    #url(r'^edit/(?P<type>[-_\w]+)/(?P<pk>[-_\w]+)$', login_required(stream_posts), name='edit_comment'),

    url(r'^comment/(?P<pk>[a-zA-Z0-9_.-]+)/edit/$', login_required(EditCommentView.as_view()), name='edit_comment'),
    url(r'^comment/(?P<pk>[a-zA-Z0-9_.-]+)/delete/$', login_required(delete_comment), name='delete_comment'),
>>>>>>> c89b346732716de05645305b62389a1a1688d43e

)