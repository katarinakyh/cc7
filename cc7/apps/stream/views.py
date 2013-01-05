from apps.event.models import Event
from apps.publication.models import Post
from apps.publication.forms import CommentForm
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from itertools import chain
from operator import attrgetter


def save_comment(request, profile):
    form = CommentForm(request.POST)
    if form.is_valid():
        form.save(commit = False)
        f=form
        f.author=profile
	"""
        if request.POST['post'] != '1':
            f.post=request.POST['post']
            form.instance.event = ''
        elif request.POST['event'] != '1':
            f.event=request.POST['event']
            form.instance.post = ''
        """
	f.save()
    else:
        print form.errors


def stream(request):
    profile = request.user.get_profile()
    if request.POST:
        if 'new_comment' in request.POST:
            save_comment(request, profile)                
     
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


