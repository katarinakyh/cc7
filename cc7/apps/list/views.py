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
from forms import ListItemForm
class ListView(ListView):
    template_name = 'list/lists.html'
    model = ItemList


class ListItemsView(CreateView):
    template_name = 'list/list_items.html'
    model = ListItem

    def get_success_url(self):
        return reverse('list_lists')

    def get_context_data(self, *args, **kwargs):
        pk = get_object_or_404(ItemList, pk=self.kwargs['pk'])

        list = ItemList.objects.get(title=pk)
        list_items = ListItem.objects.filter(item_list=pk).order_by('id')
        restricted = list.is_restricted
        user = self.request.user.pk
        your_list = False
        if (list.initiator.pk == user):
            your_list = True

        itemform = "katten"
        listform = ItemListForm()

        context = {
            'list_items': list_items,
            'list': list,
            'restricted' : restricted,
            'your_list': your_list,
            'item_from': itemform,
            'list_form': listform,
        }
        context.update(kwargs)
        return super(ListItemsView, self).get_context_data(**context)

    def post(self, request, *args, **kwargs):

        # if create
        if 'create_item' in request.POST:
            list = request.POST.get('item_list')
            order = request.POST.get('order')
            description = request.POST.get('description')
            title = request.POST.get('title')
            list = ItemList.objects.get(pk=list)

            item = ListItem.objects.create(item_list = list, key = 1)
            item.order = order
            item.description = description
            item.title = title
            # make a simple key some we can check it is the right item when change *
            key = (int(list.pk)*2*int(item.pk)*1337)
            item.key = key
            item.save()
            return HttpResponseRedirect( request.path )

        # if update
        if 'update_item' in request.POST:
            is_in_list = False
            list_f = request.POST.get('item_list')
            item_f = request.POST.get('list_item')
            order = request.POST.get('order')
            description = request.POST.get('description')
            title = request.POST.get('title')

            item = ListItem.objects.get(pk=item_f)
            list = ListItem.objects.filter(item_list=list_f)

            #if check / 10 = extra:

            if item in list:
                is_in_list = True

            key = item.key
            # * check that the data was not changed in from
            if key ==  (int(list_f)*2*int(item_f)*1337):
                if is_in_list:
                    item.order = order
                    item.description = description
                    item.title = title
                    item.save()
                else:
                    return HttpResponseRedirect( request.path )


        return HttpResponseRedirect( request.path )



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
