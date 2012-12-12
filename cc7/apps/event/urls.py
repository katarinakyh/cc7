from django.conf.urls import url, patterns
from apps.event.views import EventView, AddEventView


urlpatterns = patterns('kyhEvent.apps.event.views',
    url(r'^list/$', EventView.as_view(), name= 'list_events'),
    url(r'^add/$', AddEventView.as_view(), name= 'add_event'),         
)