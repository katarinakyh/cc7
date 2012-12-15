from models import Post
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm, DateField,  forms
from django.forms.widgets import HiddenInput
from django.forms.widgets import Textarea, DateInput

class PostForm(ModelForm):
    class Meta:
        model = Post
        widgets = {
            'body': Textarea(attrs={'cols': 200, 'rows': 10}),
        }
        #fields = ('title', 'body')
        
