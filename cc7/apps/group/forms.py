from models import Group
from django.forms import ModelForm
from apps.account.models import MyProfile

class GroupForm(ModelForm):
    model =  Group
    template_name = 'list/create_list.html'

    def form_valid(self, form):
        form.instance.inititator = self.request.user.get_profile()
        form.instance.collaborators_only = True
        form.save()

    def get_success_url(self):
        return '/group/'