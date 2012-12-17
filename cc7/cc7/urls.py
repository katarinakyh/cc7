from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import admin
from userena import views as userena_views
from apps.account.forms import EditProfileFormExtra
from apps.account.views import MyPage

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('apps.stream.urls')),
    # url(r'^cc7/', include('cc7.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/(?P<username>[\.\w]+)/$',login_required(MyPage.as_view()), name='my_page'),
    url(r'^accounts/(?P<username>[\.\w]+)/edit/$',
        userena_views.profile_edit,
        {'edit_profile_form': EditProfileFormExtra,
         },
        name='userena_profile_edit',
    ),
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^accounts/', include('userena.urls')),
    url(r'^event/', include('apps.event.urls')),
    url(r'^post/', include('apps.publication.urls')),
    url(r'^association/', include('apps.account.urls')),
    url(r'^stream/', include('apps.stream.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )