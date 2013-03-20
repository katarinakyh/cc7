from models import ItemList, ListItem
from django.forms import ModelForm
from apps.account.models import MyProfile

class ItemListForm(ModelForm):
    model =  ItemList
    template_name = 'list/create_list.html'

    def form_valid(self, form):
        form.instance.inititator = self.request.user.get_profile()
        form.instance.collaborators_only = False
        form
        form.save()

    def get_success_url(self):

        return '/list/'

class ListItemForm(ModelForm):
    model =  ListItem
    success_url = 'lists/'
    template_name = 'list/create_listitem.html'


