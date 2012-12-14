from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from models import Post
from event.models import Event
from forms import PostForm
from account.models import MyProfile

class PostView(ListView):
    template_name = 'post/events.html'
    model = Post

class AddPostView(CreateView):
    template_name = 'post/create_event.html'
    model = Post
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        post = Post.objects.creat()
        title = request.POST.get('title')
        body = request.POST.get('body')
        if (request.POST.get('is_public')):
            is_public = request.POST.get('is_public')
        if (request.POST.get('personal_page')):
            personal_page = request.POST.get('personal_page')
        if (request.POST.get('association')):
            association = request.POST.get('association')
        if (request.POST.get('event')):
            event = request.POST.get('event')

        try:
            post.title = str(title)
            post.body = str(body)
            post.author = request.user
            if (event):
                post.event = Event.object.get(event=event)
            if (association):
                post.association = Association.object.get(association=association)
            if (personal_page):
                post.personal_page = MyProfile.object.get(MyProfile=request.user)
            if (is_public):
                post.is_public = bool(is_public)

            post.save()
        except ValueError:
            pass
        
        return super(AddPostView, self).post(request, *args, **kwargs)

    def get_success_url(self):

        return reverse('my_page')
