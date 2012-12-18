from django.conf.urls.defaults import *
from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from views import my_page


urlpatterns = patterns('apps.account.views',
    url(r'^$', 'my_page', name = 'my_page'),
)