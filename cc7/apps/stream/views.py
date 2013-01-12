from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from apps.event.models import Event
from apps.publication.models import Post
from apps.publication.forms import CommentForm, MessageForm
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from itertools import chain
from operator import attrgetter



def save_comment(request, profile):
    """
    Saves a comment to the stream
    """
    form = CommentForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author=profile
        instance.save()
    else:
        print form.errors


def stream(request):
    """
    Handles posts and publications in the personal stream.
    """
    profile = request.user.get_profile()

    if request.POST and 'new_comment' in request.POST:
        save_comment(request, profile)
        return HttpResponseRedirect(reverse('stream'))
     
    posts = Post.objects.filter(is_public=True).order_by('-date_created')
    events = Event.objects.filter().order_by('-date_created')
    comment_form = CommentForm()
    result_list =  sorted(chain(posts, events), key=attrgetter('date_created'))

    return render_to_response('stream/stream.html', {
            'object_list': result_list,
            'comment_form': comment_form,
            'profile': profile,
        }, context_instance=RequestContext(request))

def stream_posts(request):
    profile = request.user.get_profile()
    if request.POST:
        if 'new_comment' in request.POST:
            save_comment(request, profile)

    posts = Post.objects.filter(is_public=True).order_by('-date_created')
    comment_form = CommentForm()

    return render_to_response('stream/stream.html', {
        'object_list': posts,
        'comment_form': comment_form,
        'profile': profile,
        }, context_instance=RequestContext(request))

def stream_events(request):
    profile = request.user.get_profile()
    if request.POST:
        if 'new_comment' in request.POST:
            save_comment(request, profile)

    events = Event.objects.filter().order_by('-date_created')
    comment_form = CommentForm()

    return render_to_response('stream/stream.html', {
        'object_list': events,
        'comment_form': comment_form,
        'profile': profile,
        }, context_instance=RequestContext(request))


