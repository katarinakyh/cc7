from django.conf.urls import url, patterns
from apps.accounts.views import AccountsView, AddAccountView


urlpatterns = patterns('cc7.apps.accounts.views',
    url(r'^$', AssocationsView.as_view(), name= 'list_associations'),

)