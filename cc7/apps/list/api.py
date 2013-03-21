from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization

from tastypie import fields
from models import ListItem, ItemList


class ItemListResource(ModelResource):
    class Meta:
        queryset = ItemList.objects.all()
        resource_name = 'itemlist'
        allowed_methods = ['get','post']
        always_return_data = True
        authorization= Authorization()

        #authentication = BasicAuthentication()
        #authorization = DjangoAuthorization()

class ListItemResource(ModelResource):
    item_list = fields.ForeignKey('apps.list.api.ItemListResource', 'item_list', full=True)

    class Meta:
        queryset = ListItem.objects.all()
        resource_name = 'listitem'
        allowed_methods = ['get', 'post', 'put', 'delete']
        always_return_data = True
        authorization= Authorization()
        #authentication = BasicAuthentication()
        #authorization = DjangoAuthorization()
