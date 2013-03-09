from django.conf.urls import url, include, patterns
from django.contrib.auth.decorators import login_required
from api import ImageResource
from tastypie.api import Api
from views import upload_file

v1 = Api('v1')
v1.register(ImageResource())

urlpatterns = patterns('',
    url(r'^api/', include(v1.urls)),
    url(r'^upload_file/$', login_required(upload_file), name= 'upload_file'),
)
