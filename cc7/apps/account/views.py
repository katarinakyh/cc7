from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse
from models import Association
from forms import AssociationForm

class MyPage(TemplateView):
    template_name = 'base.html'

class AssociationView(ListView):
    template_name = 'account/associations.html'
    model = Association

class AddPostView(CreateView):
    template_name = 'account/create_association.html'
    model = Post
    form_class = PostForm

    def post(self, request, *args, **kwargs):

        self.object = None

        return super(AddPostView, self).post(request, *args, **kwargs)

    def get_success_url(self):

        return reverse('my_page')