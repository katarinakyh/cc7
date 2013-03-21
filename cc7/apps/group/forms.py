from models import Group
from django.forms import ModelForm
from apps.account.models import MyProfile
from apps.publication.models import Post

class GroupForm(ModelForm):
    model = Group
    template_name = 'list/create_list.html'

    def form_valid(self, form):
        form.instance.inititator = self.request.user.get_profile()
        form.instance.collaborators_only = True
        form.save()

    def get_success_url(self):
        return '/group/'

class GroupPostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('event','association', 'image')
        fields = ('title', 'body','is_public')

    def form_valid(self, form):
        #form.instance.author = self.request.user.get_profile()
        form.save()



    def get_success_url(self):
        return '/group/'
