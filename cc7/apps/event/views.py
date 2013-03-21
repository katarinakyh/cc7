from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from models import Event
from forms import EventForm, EventCommentForm
from apps.publication.forms import CommentForm
from apps.stream.views import save_comment

class EventView(ListView):
    """
    This is not used, stream/view stream_events
    """
    template_name = 'stream/event_stream.html'
    model = Event
    form_class = EventCommentForm


class AddEventView(CreateView):
    template_name = 'event/create_event.html'
    model = Event
    form_class = EventForm
    
    def get_success_url(self):
        return reverse('stream_events')

class EventDetailView(DetailView):
    model = Event
    form_class = CommentForm

def event_detail(request, pk):
    profile = request.user.get_profile()
    if request.POST:
        if 'new_comment' in request.POST:
            save_comment(request, profile)
            return HttpResponseRedirect(reverse('show_event', args=(pk,)))
    
    else:    
        event = Event.objects.get(pk=pk)
        comment_form = CommentForm()
    
        return render(request, 'event/event_detail.html', {
                'comment_form': comment_form,
                'post': event,
                'profile': profile,
            })