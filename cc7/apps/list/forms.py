from models import ItemList, ListItem
from django.forms import ModelForm


class ItemListForm(ModelForm):
    class Meta:
        model =  ItemList

class ListItemForm(ModelForm):
    model =  ListItem
    success_url = 'lists/'
    template_name = 'list/create_listitem.html'


