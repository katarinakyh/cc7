from itertools import chain
from operator import attrgetter
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Post, Comment, Message
from .forms import ThreadForm, CommentForm, MessageForm, CommentEditForm
from apps.account.models import MyProfile
from apps.stream.views import save_comment


class EditCommentView(UpdateView):
    """ Editing of a users commentin the stream.
        TODO: Verify only authorized users can edit form
    """
    model = Comment
    form_class = CommentEditForm
    template_name = 'publication/edit_comment.html'

    def get_success_url(self):
        return '/' # self.request.META.get('referer')


def delete_post(request, model, pk):
    profile = request.user.get_profile()            
<<<<<<< HEAD
    
    if model == 'comment':
        post = Comment.objects.get(pk=pk)
    elif model == 'post':
        post = Post.objects.get(pk=pk)
    elif model == 'message':
        post = Message.objects.get(pk=pk)

    if post.author == profile:
        post.delete()    
        return HttpResponseRedirect('/')

def edit_post(request, model, pk):
    profile = request.user.get_profile()            
    
    if model == 'comment':
        post = Comment.objects.get(pk=pk)
        form = CommentForm(instance=post)
    elif model == 'post':
        post = Post.objects.get(pk=pk)
        form = PostForm(instance=post)
    elif model == 'message':
        post = Message.objects.get(pk=pk)
        form = MessageForm(instance=post)

    if post.author == profile:
        print ''
        if request.POST:
            if model == 'comment':
                form = CommentForm(request.POST, instance=post)
            elif model == 'post':
                form = PostForm(request.POST, instance=post)
            elif model == 'message':
                form = MessageForm(request.POST,instance=post)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/')
    

        return render(request, 'publication/change_post.html', {
                'model':model,
                'form': form,
                'post': post,
                'profile': profile,
            })    
    else:
        return HttpResponseRedirect('/')
        

=======
    comment = Comment.objects.get(pk=pk)
    if comment.author == profile:
        comment.delete()
        return HttpResponseRedirect('/')

>>>>>>> c89b346732716de05645305b62389a1a1688d43e
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
    """ Add a post to the stream
    """
    model = Post
    form_class = ThreadForm
    success_url = '/'
    template_name = 'publication/create_post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.get_profile()
        form.instance.is_public = True
        form.instance.title = self.request.POST.get('title')
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
