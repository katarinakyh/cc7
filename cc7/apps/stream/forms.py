from cc7.publication.models import Comment
from django.forms import ModelForm

class CommentForm(ModelForm):
    class Meta:
        model = Comment
