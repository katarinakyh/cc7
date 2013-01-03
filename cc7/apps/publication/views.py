from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, CreateView
from django.views.generic import View, DetailView
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import render
from models import Post, Comment
from apps.event.models import Event
from forms import PostForm, ThreadForm, CommentForm
from apps.account.models import MyProfile, Association
from django.contrib.auth.models import User
from apps.stream.views import save_comment


class PostView(ListView):
    template_name = 'stream/stream.html'
    model = Post


class AddPostView(FormView):
    template_name = 'publication/create_post.html'
    model = Post
    form_class = ThreadForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user.get_profile()
        form.instance.is_public = True
        form.save()
        return super(AddPostView, self).form_valid(form)
    
def post_detail(request, pk):
    profile = request.user.get_profile()
    if request.POST:
        if 'new_comment' in request.POST:
            save_comment(request, profile)
            print 'newcomment'
            
    post = Post.objects.get(pk=pk)
    comment_form = CommentForm()

    return render(request, 'publication/post_detail.html', {
            'comment_form': comment_form,
            'post': post,
            'profile': profile,
        })


"""

class PostDetailView(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = {
            'form': CommentForm(),
            'profile': self.request.user.get_profile(),
        }
        context.update(kwargs)
        return super(PostDetailView, self).get_context_data(**context)
 
class PostComment(FormView, SingleObjectMixin):
    template_name = 'publication/post_detail.html'
    form_class = CommentForm
    model = Post
    success_url = '/'

    print 'in here now y all'

    
    def get_context_data(self, **kwargs):
        context = {
            'object': self.get_object(),
        }
        return super(PostComment, self).get_context_data(**context)
     
    def get_success_url(self):
        print 'yo'
        return reverse('postdetailview',{kwargs:self.get_context_data(),})
    
    def form_valid(self, form):
        save_comment(self.request, self.request.user.get_profile())

class PostDetail(View):

    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print 'in post'
        view = PostComment.as_view()
        return view(request, *args, **kwargs)
"""