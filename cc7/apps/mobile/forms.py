from apps.publication.models import Post

from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from django.forms.widgets import Textarea, TextInput, FileInput
from apps.account.models import MyProfile


class MobileForm(ModelForm):
    class Meta:
        model= Post
        widgets = {
            'body': Textarea(attrs={'placeholder': 'body'}),
            'title': TextInput(attrs={'placeholder': 'title'}),
            'image': FileInput(attrs={'placeholder': 'image'})

        }
        exclude = ('author','event','association','is_public',)
        fields = ('title', 'body', 'image',)

