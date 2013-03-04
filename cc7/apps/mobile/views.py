from django.views.generic.base import TemplateView
from apps.stream.views import stream

class PostsView(TemplateView):
    template_name = 'mobile/post.html'


