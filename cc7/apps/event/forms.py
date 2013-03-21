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

    def form_valid(self, form):
        form.instance.inititator = self.request.user.get_profile()
        form.instance.collaborators_only = True
        form.save()

class EventCommentForm(ModelForm):
    class Meta:
        model = Post
