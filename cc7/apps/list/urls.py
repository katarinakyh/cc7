from django.conf.urls import url, patterns, include
from django.contrib.auth.decorators import login_required
from views import ListView, ListViewCreate, ListItemsView, ListItemViewCreate, ItemListDetailView

urlpatterns = patterns('cc7.apps.list.views',
    url(r'^$', login_required(ListView.as_view()), name= 'list_lists'),
    url(r'^create/$', login_required(ListViewCreate.as_view()), name= 'create_list'),
    url(r'^create_item/$', login_required(ListItemViewCreate.as_view()), name= 'create_list_item'),
    url(r'^(?P<pk>[-_\w]+)/$', login_required(ListItemsView.as_view()), name='show_list'),
)
