from models import Event
from django.contrib.admin.widgets import AdminDateWidget
from django.forms import ModelForm, DateField
from django.forms.widgets import Textarea, DateInput
from apps.publication.models import Post


class EventForm(ModelForm):
    class Meta:
        model = Event
        widgets = {
            'description': Textarea(attrs={'cols': 180, 'rows': 7}),
        }

class EventCommentForm(ModelForm):
    class Meta:
        model = Post
