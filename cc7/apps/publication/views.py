from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
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

class AddPostView(CreateView):
    template_name = 'publication/create_post.html'
    model = Post
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        post = Post()
        title = request.POST.get('title')
        body = request.POST.get('body')
        if (request.POST.get('is_public')):
            is_public = request.POST.get('is_public')
        else:
            is_public = 0
        if (request.POST.get('personal_page')):
            personal_page = request.POST.get('personal_page')
        else:
            personal_page = 0

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
            if (personal_page != 0):
                post.personal_page = user
            if (is_public != 0):
                post.is_public = bool(is_public)

            post.save()
        except ValueError:
            pass

        return super(AddPostView, self).post(request, *args, **kwargs)

    def get_success_url(self):

        return reverse('my_page')

class PostDetailView(DetailView):
    model = Post
