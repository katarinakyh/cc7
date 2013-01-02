from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.views.generic import DetailView
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from models import Post, Message
from apps.event.models import Event
from forms import PostForm, ThreadForm, MessageForm
from apps.account.models import MyProfile, Association
from django.contrib.auth.models import User
from itertools import chain
from operator import attrgetter


class PostView(ListView):
    template_name = 'stream/stream.html'
    model = Post

class AddMessageView(FormView):
    template_name = 'publication/create_message.html'
    model = Message
    form_class = MessageForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = {
            'alluser':MyProfile.objects.all()
        }
        context.update(kwargs)
        return super(AddMessageView, self).get_context_data(**context)

    def form_valid(self, form):
        form.instance.author = self.request.user.get_profile()
        form.instance.is_public = False
        form.instance.to = MyProfile.objects.get(user__username = self.request.POST.get('name'))
        form.save()
        return super(AddMessageView, self).form_valid(form)

class AddPostView(FormView):
    template_name = 'publication/create_post.html'
    model = Post
    form_class = ThreadForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.thread = form.instance.pk
        form.instance.author = self.request.user.get_profile()
        form.instance.is_public = True
        form.save()
        return super(AddPostView, self).form_valid(form)


class MessageView(ListView):
    template_name = 'publication/messages.html'
    model = Message

    def get_context_data(self, **kwargs):
        from_me = Message.objects.filter(author=self.request.user).order_by('-date_created')
        to_me = Message.objects.filter(to=self.request.user).order_by('-date_created')
        message_list =  sorted(chain(from_me, to_me),key=attrgetter('date_created'))
        context = {
            'from_me':from_me,
            'to_me':to_me,
            'message_list':message_list
        }
        context.update(kwargs)
        return super(   MessageView, self).get_context_data(**context)

def view_message(request, pk):
    message = Message.objects.get(pk=pk)
    thread = Message.objects.filter(thread=message.thread)
    form = MessageForm()
    return render_to_response('publication/message_thread.html', {
        'message_list': thread,
        'form': form,
        }, context_instance=RequestContext(request))

"""
    def post(self, request, *args, **kwargs):
        post = PostForm(request.POST)
        if post.is_valid():
            post = post.save(commit=False)
            title = request.POST.get('title')
            body = request.POST.get('body')
            if (request.POST.get('is_public')):
                is_public = request.POST.get('is_public')
            else:
                is_public = 0

            if (request.POST.get('association')):
                association = request.POST.get('association')
            else:
                association = 0

            if (request.POST.get('event')):
                event = request.POST.get('event')
            else:
                event = 0

            user = User.objects.get(username=request.user)

            try:
                post.title = str(title)
                post.body = str(body)
                post.author = MyProfile.objects.get(user=user)
                if (event != 0):
                    post.event = Event.objects.get(id=event)
                if (association != 0):
                    post.association = Association.objects.get(id=association)
                if (is_public != 0):
                    post.is_public = bool(is_public)

                #post.save()
            except ValueError:
                pass

            return super(AddPostView, self).post(request, *args, **kwargs)


    def get_success_url(self):

        return reverse('stream')
"""
class PostDetailView(DetailView):
    model = Post
