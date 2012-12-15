from django.conf.urls import url, patterns
from django.contrib.auth.decorators import login_required
from apps.account.views import AssociationView


urlpatterns = patterns('cc7.apps.accounts.views',
    url(r'^$', login_required(AssociationView.as_view()), name= 'list_associations'),

)