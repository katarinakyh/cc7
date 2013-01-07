from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from django.shortcuts import render
from models import Event
from forms import EventForm, EventCommentForm
from apps.publication.forms import CommentForm
from apps.stream.views import save_comment

class EventView(ListView):
    template_name = 'stream/stream.html'
    model = Event
    form_class = EventCommentForm

class AddEventView(CreateView):
    template_name = 'event/create_event.html'
    model = Event
    form_class = EventForm
    
    def get_success_url(self):
        return reverse('list_events')

class EventDetailView(DetailView):
    model = Event
    form_class = CommentForm()


def event_detail(request, pk):
    profile = request.user.get_profile()
    if request.POST:
        if 'new_comment' in request.POST:
            save_comment(request, profile)
            
    event = Event.objects.get(pk=pk)
    print event
    comment_form = CommentForm()

    return render(request, 'event/event_detail.html', {
            'comment_form': comment_form,
            'post': event,
            'profile': profile,
        })
