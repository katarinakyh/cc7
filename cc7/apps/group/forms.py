from models import Group, ActiveMember
from django.forms import ModelForm
from apps.account.models import MyProfile
from apps.publication.models import Post

class GroupForm(ModelForm):
    class Meta:
        model = Group
        template_name = 'list/create_list.html'

    def get_success_url(self):
        return '/group/1'

class GroupPostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('event','association', 'image')
        fields = ('title', 'body','is_public')

    def form_valid(self, form):
        #form.instance.author = self.request.user.get_profile()
        print "hus"
        form.save()

    def get_success_url(self):
        return '/group/1'

class JoinGroupForm(ModelForm):
    class Meta:
        model = ActiveMember
