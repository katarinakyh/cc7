from django.conf.urls import url, patterns, include
from django.contrib.auth.decorators import login_required
from views import GroupListView, GroupCreateView, GroupDetailView,GroupUpdateView

urlpatterns = patterns('cc7.apps.list.views',
    url(r'^$', login_required(GroupListView.as_view()), name= 'list_groups'),
    url(r'^create_group/$', login_required(GroupCreateView.as_view()), name= 'create_group'),
    url(r'^update_group/(?P<pk>[-_\w]+)/$', login_required(GroupUpdateView.as_view()), name= 'update_group'),
    url(r'^(?P<pk>[-_\w]+)/$', login_required(GroupDetailView.as_view()), name='detail_group'),
)
