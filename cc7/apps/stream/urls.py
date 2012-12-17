from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from apps.stream.views import Stream


urlpatterns = patterns('cc7.apps.stream.views',
    url(r'^$', login_required(Stream), name='stream'),
)
