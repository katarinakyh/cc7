from tastypie import fields
from tastypie.resources import ModelResource
from models import Image

class ImageResource(ModelResource):
    img = fields.FileField(attribute="image", null=True, blank=True)
    class Meta:
        queryset = Image.objects.all()
        allowed_methods = ['get', 'post']

