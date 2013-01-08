from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from apps.event.views import EventView, AddEventView, EventDetailView, event_detail
from apps.stream.views import stream_events

urlpatterns = patterns('cc7.apps.event.views',
    url(r'^list/$', login_required(EventView.as_view()), name= 'list_events'),
    url(r'^add/$', login_required(AddEventView.as_view()), name= 'add_event'),
    url(r'^detail/(?P<pk>[-_\w]+)/$', login_required(event_detail), name='eventdetailview'),
    url(r'^filter/$', login_required(stream_events), name= 'stream_events'),
)