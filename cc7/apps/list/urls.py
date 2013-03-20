from django.conf.urls import url, patterns, include
from django.contrib.auth.decorators import login_required
from views import ListView, ListViewCreate, ListItemsView, ListItemViewCreate, ItemListDetailView
from api import ListItemResource, ItemListResource
from tastypie.api import Api

v1 = Api('v1')
v1.register(ListItemResource())
v1.register(ItemListResource())



urlpatterns = patterns('cc7.apps.list.views',
    url(r'^api/', include(v1.urls)),
    url(r'^$', login_required(ListView.as_view()), name= 'list_lists'),
    url(r'^create/$', login_required(ListViewCreate.as_view()), name= 'create_list'),
    url(r'^create_item/$', login_required(ListItemViewCreate.as_view()), name= 'create_list_item'),
    url(r'^(?P<pk>[-_\w]+)/$', login_required(ListItemsView.as_view()), name='show_list'),
)
