from models import ItemList, ListItem
from django.views.generic import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from forms import ItemListForm
from django.template import RequestContext
from django.shortcuts import get_object_or_404

class ListView(ListView):
    template_name = 'list/lists.html'
    model = ItemList

class ListItemsView(ListView):
    template_name = 'list/list_items.html'
    model = ItemList
    #form_class = CommentForm

    def get_context_data(self, *args, **kwargs):
        pk = get_object_or_404(ItemList, pk=self.kwargs['pk'])

        list = ItemList.objects.get(title=pk)
        list_items = ListItem.objects.filter(item_list=pk).order_by('id')


        context = {
            'list_items': list_items,
            'list': list
        }
        context.update(kwargs)
        return super(ListItemsView, self).get_context_data(**context)

class ListViewCreate(CreateView):
    template_name = 'list/create_list.html'
    model = ItemList
    #form_class = ItemListForm


    def get_success_url(self):
        return reverse('list_lists')

class ListItemViewCreate(CreateView):
    template_name = 'list/create_list.html'
    model = ListItem
    #form_class = ItemListForm

    def get_success_url(self):
        return reverse('list_lists')



class ItemListDetailView(DetailView):
    model = ItemList
    #form_class = CommentForm


class ListActivityBase(RedirectView):
    def get(self, request, *args, **kwargs):
        list = ItemList.objects.get(slug=kwargs.get('slug'))
        self.update_action(request, list, request.user.get_profile())
        success_url = request.META.get('referer') or '/list//'

        print 'groups', request.user.get_profile().itemlist.all()
        return HttpResponseRedirect(success_url)

class ListJoinView(ListActivityBase):
    """
    Lets a user join an List (group)
    """
    def update_action(self, request, list, user_profile):
        if list not in user_profile.list.all():
            user_profile.list.add(list)
            user_profile.save()
            messages.success(request, u'Joined group')

class ListLeaveView(ListActivityBase):
    """
    Lets a user leave an List (group)
    """
    def update_action(self, request, list, user_profile):
        if list in user_profile.list.all():
            user_profile.list.remove(list)
            user_profile.save()
            messages.success(request, u'Left group')
