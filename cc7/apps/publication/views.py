from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from models import Post
from apps.event.models import Event
from forms import PostForm, ThreadForm
from apps.account.models import MyProfile, Association
from django.contrib.auth.models import User


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
