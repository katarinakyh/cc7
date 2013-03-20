from tastypie import fields
from tastypie.resources import ModelResource
from models import Image
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication

class ImageResource(ModelResource):
    img = fields.FileField(attribute="image", null=True, blank=True)
    class Meta:
        queryset = Image.objects.all()
        allowed_methods = ['get', 'post']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()


