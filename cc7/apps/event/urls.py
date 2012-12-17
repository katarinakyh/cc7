from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from apps.event.views import EventView, AddEventView, EventDetailView


urlpatterns = patterns('cc7.apps.event.views',
    url(r'^list/$', login_required(EventView.as_view()), name= 'list_events'),
    url(r'^add/$', login_required(AddEventView.as_view()), name= 'add_event'),
    url(r'^detail/(?P<pk>[-_\w]+)/$', login_required(EventDetailView.as_view()), name='eventdetailview'),
)