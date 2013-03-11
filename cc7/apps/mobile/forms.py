from apps.publication.models import Post

from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from django.forms.widgets import Textarea, DateInput
from apps.account.models import MyProfile


class MobileForm(ModelForm):
    class Meta:
        model= Post
        widgets = {
            'body': Textarea(attrs={'cols': 200, 'rows': 10}),
            }
        exclude = ('author','event','association','is_public',)
        fields = ('title', 'body', 'image',)

