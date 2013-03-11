from django.views.generic.base import TemplateView
from apps.stream.views import stream
from django.views.generic.edit import FormView
from apps.publication.models import Post
from forms import MobileForm

class PostsView(TemplateView):
    template_name = 'mobile/post.html'


class AddPostView(FormView):
    model = Post
    form_class = MobileForm
    success_url = '/mobile/'
    template_name = 'mobile/create_post.html'


    def form_valid(self, form):
        self.request.POST.get('image')
        form.instance.author = self.request.user.get_profile()
        form.instance.is_public = True
        form.instance.title = self.request.POST.get('title')
        form.save()
        return super(AddPostView, self).form_valid(form)
