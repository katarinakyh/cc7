
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from apps.event.models import Event
from apps.publication.models import Post
from apps.publication.forms import CommentForm, MessageForm
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from itertools import chain
from operator import attrgetter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    #events = Event.objects.filter().order_by('date_created')
    comment_form = CommentForm()
    #result_list =  sorted(chain(posts, events))
    #pagination

    page_list = pagination(request, posts)

    return render_to_response('stream/stream.html', {
            'object_list': page_list,
            'comment_form': comment_form,
            'profile': profile,
        }, context_instance=RequestContext(request))


def pagination(request, list):
    paginator = Paginator(list, 20) # Show 20 contacts per page

    page = request.GET.get('page')

    try:
        page_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        page_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        page_list = paginator.page(1)

    return page_list


def stream_posts(request):
    profile = request.user.get_profile()
    if request.POST:
        if 'new_comment' in request.POST:
            save_comment(request, profile)
            print 'I am here'
            return HttpResponseRedirect(reverse('stream_posts'))

    posts = Post.objects.filter(is_public=True).order_by('-date_created')
    comment_form = CommentForm()

    page_list = pagination(request, posts)

    return render_to_response('stream/post_stream.html', {
        'object_list': page_list,
        'comment_form': comment_form,
        'profile': profile,
        }, context_instance=RequestContext(request))

def stream_events(request):
    profile = request.user.get_profile()
    if request.POST:
        if 'new_comment' in request.POST:
            save_comment(request, profile)
            return HttpResponseRedirect(reverse('stream_events'))

    events = Event.objects.filter().order_by('-date_created')
    comment_form = CommentForm()

    page_list_events = pagination(request, events)

    return render_to_response('stream/event_stream.html', {
        'object_list': page_list_events ,
        'comment_form': comment_form,
        'profile': profile,
        }, context_instance=RequestContext(request))


