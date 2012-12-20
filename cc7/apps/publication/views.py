from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from models import Post
from apps.event.models import Event
from forms import PostForm
from apps.account.models import MyProfile, Association
from django.contrib.auth.models import User


class PostView(ListView):
    template_name = 'stream/stream.html'
    model = Post


class AddPostView(FormView):
    template_name = 'publication/create_post.html'
    model = Post
    form_class = PostForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user.get_profile()
        form.instance.is_public = True
        form.save()
        return super(AddPostView, self).form_valid(form)


class PostDetailView(DetailView):
    model = Post