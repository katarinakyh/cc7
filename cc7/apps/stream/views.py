from apps.event.models import Event
from apps.publication.models import Post
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from itertools import chain
from operator import attrgetter

def stream(request):
    posts = Post.objects.filter().order_by('-date_created')
    events = Event.objects.filter().order_by('-date_created')
    result_list =  sorted(chain(posts, events),
        key=attrgetter('date_created'))
    return render_to_response('stream/stream.html', {
        'object_list': result_list,
        }, context_instance=RequestContext(request))


