from django.core.urlresolvers import reverse 
from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import admin
from userena import views as userena_views
from apps.account.forms import EditProfileFormExtra, SignupFormExtra, PasswordChangeFormExtra
from apps.account.views import AssociationView
from apps.publication.views import MessageView
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('apps.stream.urls')),
    url(r'^accounts/signup/$',
       userena_views.signup,
        {
            'signup_form':SignupFormExtra,
        },
       name='userena_signup'),
    url(r'^accounts/(?P<username>[\.\w]+)/password/$',
       userena_views.password_change,
       {
        'pass_form': PasswordChangeFormExtra,      
        },
       name='userena_password_change'),

    url(r'^accounts/(?P<username>(?!signout|signup|signin)[\.\w]+)/$', include('apps.account.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/(?P<username>[\.\w]+)/edit/$',
        userena_views.profile_edit,
        {
            'edit_profile_form': EditProfileFormExtra,
        },
        name='userena_profile_edit',
    ),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^accounts/', include('userena.urls')),
    url(r'^post/', include('apps.publication.urls')),
    url(r'^messages/', login_required(MessageView.as_view()), name='show_messages'),
    url(r'^message/(?P<pk>[a-zA-Z0-9_.-]+)/$', 'apps.publication.views.view_message', name='show_message_thread'),
    url(r'^event/', include('apps.event.urls')),
    url(r'^association/(?P<association>[a-zA-Z0-9_.-]+)/$', 'apps.account.views.my_page', name='show_association'),
    url(r'^association/', login_required(AssociationView.as_view()), name='list_associations'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )