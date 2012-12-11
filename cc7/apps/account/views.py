from django.views.generic import TemplateView

class MyPage(TemplateView):
    template_name = 'base.html'