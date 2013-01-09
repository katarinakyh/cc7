from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView
from django.views.generic import View, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from models import Post, Comment, Message
from apps.event.models import Event
from forms import PostForm, ThreadForm, CommentForm, MessageForm
from apps.account.models import MyProfile, Association
from django.contrib.auth.models import User
from apps.stream.views import save_comment
from itertools import chain
from operator import attrgetter, itemgetter


class PostView(ListView):
    template_name = 'stream/stream.html'
    model = Post

class AddMessageView(FormView):
    template_name = 'publication/create_message.html'
    model = Message
    form_class = MessageForm
    success_url = '/messages/'
    
    def get_context_data(self, **kwargs):
        context = {
            'alluser':MyProfile.objects.all()
        }
        context.update(kwargs)
        return super(AddMessageView, self).get_context_data(**context)

    def form_valid(self, form):
        try:
            last_message= Message.objects.latest('pk')
            thread = int(last_message.pk)+1
        except:
            thread=1
        
        form.save(commit=False)
        form.instance.author = self.request.user.get_profile()
        form.instance.thread = thread
        try:
            form.instance.to = MyProfile.objects.get(user__username = self.request.POST.get('name'))
        except:
            pass
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
    
def post_detail(request, pk):
    profile = request.user.get_profile()
    if request.POST:
        if 'new_comment' in request.POST:
            save_comment(request, profile)
            
    post = Post.objects.get(pk=pk)
    comment_form = CommentForm()

    return render(request, 'publication/post_detail.html', {
            'comment_form': comment_form,
            'post': post,
            'profile': profile,
        })

class MessageView(ListView):
    template_name = 'publication/messages.html'
    model = Message


    def get_context_data(self, **kwargs):
        from_me = Message.objects.filter(author=self.request.user).order_by('-date_created')
        to_me = Message.objects.filter(to=self.request.user).order_by('-date_created')
        message_list =  sorted(chain(from_me, to_me),key=attrgetter('date_created'))
        message_list = sorted(message_list, reverse=False)

        context = {
            'from_me':from_me,
            'to_me':to_me,
            'message_list':message_list
        }
        context.update(kwargs)
        return super(MessageView, self).get_context_data(**context)


    def get_context_data(self, **kwargs):
        profile = self.request.user.get_profile()
        from_me = Message.objects.filter(author=profile).order_by('-date_created')
        to_me = Message.objects.filter(to=profile).order_by('-date_created')
        message_list =  sorted(chain(from_me, to_me),key=attrgetter('date_created'))
        message_list.sort(key=lambda x: x.date_created, reverse=True)
        result_list = sorted(message_list, key=lambda x: x.date_created, reverse=True)

        m_list = []
        thread=[]

        for m in result_list:
            if m.thread not in thread:
                thread.append(m.thread)
                m_list.append(m)

            context = {
            'profile':profile,
            'm_list':m_list,
        }

        context.update(kwargs)
        return super(MessageView, self).get_context_data(**context)


def view_message(request, pk):
    profile=request.user.get_profile()
    messages = Message.objects.filter(thread=pk)
    if ((messages[0].to == profile) or (messages[0].author == profile)):
        if request.POST:
            form = MessageForm(request.POST)
            if form.is_valid():                
                form.save(commit=False)
                f = form
                f.author = profile
                f.save()
            else:
                print form.errors
    
        message_list = Message.objects.filter(thread=pk).order_by('-date_created')
        message_form = MessageForm()

        return render_to_response('publication/message_thread.html', {
            'message_list': message_list,
            'message_form': message_form,
            'profile':profile,
            }, context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect('/messages/')
