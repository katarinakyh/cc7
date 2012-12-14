from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from models import Post
from forms import PostForm

class PostView(ListView):
    template_name = 'post/events.html'
    model = Post

class AddPostView(CreateView):
    template_name = 'post/create_event.html'
    model = Post
    form_class = PostForm

    def post(self, request, *args, **kwargs):

        self.object = None

        return super(AddPostView, self).post(request, *args, **kwargs)

    def get_success_url(self):

        return reverse('my_page')