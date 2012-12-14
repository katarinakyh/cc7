from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from models import Event
from forms import EventForm

class EventView(ListView):
    template_name = 'event/events.html'
    model = Event
    
class AddEventView(CreateView):
    template_name = 'event/create_event.html'
    model = Event
    form_class = EventForm
    
    def get_success_url(self):
        return reverse('list_events')