from models import Post, Comment, Message
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm, DateField, forms
from django.forms.widgets import HiddenInput
from django.forms.widgets import Textarea, DateInput
from models import Post, Comment
from apps.account.models import MyProfile


class PostForm(ModelForm):
    class Meta:
        model = Post
        widgets = {
            'body': Textarea(attrs={'cols': 200, 'rows': 10}),
            'author': HiddenInput()
        }
        fields = ('title', 'body', 'image', 'author')
                
class CommentForm(ModelForm):
    class Meta:
        model = Comment

class CommentEditForm(ModelForm):

    class Meta:
        model = Comment
        widgets = {
            'author': HiddenInput()
        }

        exclude = ( 'date_created', 'post', 'event')


class MessageForm(ModelForm):
    class Meta:
        model = Message
        widgets = {
            'body': Textarea(attrs={'cols': 300, 'rows': 10}),
        }

    def clean_to(self):
        name  = self.cleaned_data['to']
        friends = MyProfile.objects.all()
        if name not in friends:
            raise forms.ValidationError("This profile does not exist")

        return name

class ThreadForm(ModelForm):
    class Meta:
        model= Post
        widgets = {
            'body': Textarea(attrs={'cols': 200, 'rows': 10}),
        }
        exclude = ('author','event','association','is_public',)
        fields = ('title', 'body', 'image',)

