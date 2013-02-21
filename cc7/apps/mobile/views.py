from django.views.generic.base import TemplateView


class PostsView(TemplateView):
    template_name = 'mobile/post.html'


