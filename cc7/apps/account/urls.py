from django.conf.urls.defaults import *
from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from views import my_page, AssociationJoinView, AssociationLeaveView, AssociationView


urlpatterns = patterns('apps.account.views',
    url(r'^$', 'my_page', name = 'my_page'),

    url(r'^/', login_required(AssociationView.as_view()), name='list_associations'),
    url(r'^(?P<association>[a-zA-Z0-9_.-]+)/$', 'my_page', name='show_association'),
    url(r'^(?P<slug>[-\w]*)/join/$', AssociationJoinView.as_view(), name='join_association'),
    url(r'^(?P<slug>[-\w]*)/leave/$', AssociationLeaveView.as_view(), name='leave_association'),

)