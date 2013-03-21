from models import Group, ActiveMember
from forms import GroupForm
from django.views.generic import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_object_or_404

class GroupListView(ListView):
    template_name = 'group/groups.html'
    model = Group

class GroupDetailView(DetailView):
    template_name = 'group/group_detail.html'
    model = Group

    def get_context_data(self, **kwargs):
        pk = get_object_or_404(Group, pk=self.kwargs['pk'])

        group = Group.objects.get(title=pk)
        is_member =  ActiveMember.objects.mygroups(self.request, group)
        user = self.request.user.get_profile()
        user_id = user.pk
        group_pk = group.pk
        active_members = ActiveMember.objects.filter(group=group_pk, is_member = True)
        pending_members = ActiveMember.objects.filter(group=group_pk, is_member = False)
        membership_active = ActiveMember.objects.filter(group=group_pk, is_member = True, member = user )
        membership_pending = ActiveMember.objects.filter(group=group_pk,  is_member = False, member = user)
        if (membership_active or membership_pending):
            can_request_membership = False
        else:
            can_request_membership = True

        context = {
            'group_object': group,
            'members': active_members,
            'pending': pending_members,
            'membership_active':membership_active,
            'membership_pending':membership_pending,
            'can_request_membership': can_request_membership,
            'user_id':user_id
        }
        context.update(kwargs)
        return super(GroupDetailView, self).get_context_data(**context)


class GroupCreateView(CreateView):
    template_name = 'group/create_group.html'
    model = Group
    #form_class = GroupForm
    success_url = '/group/'

class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'group/update_group.html'

    def get(self, request, **kwargs):
        self.object = Group.objects.get(pk=self.kwargs['pk'])
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def form_valid(self, form):
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class GroupActivityBase(RedirectView):
    def get(self, request, *args, **kwargs):
        group = Group.objects.get(pk=kwargs.get('pk'))
        self.update_action(request, group, request.user.get_profile())
        success_url = request.META.get('referer') or '/group/'

        print 'groups', request.user.get_profile().itemlist.all()
        return HttpResponseRedirect(success_url)

class GroupJoinView(GroupActivityBase):
    """
    Lets a user join an List (group)
    """
    def update_action(self, request, group, user_profile):
        if group not in user_profile.list.all():
            user_profile.group.add(group)
            user_profile.save()
            #messages.success(request, u'Joined group')

class GroupLeaveView(GroupActivityBase):
    """
    Lets a user leave an List (group)
    """
    def update_action(self, request, group, user_profile):
        if list in user_profile.group.all():
            user_profile.group.remove(list)
            user_profile.save()
            ##messages.success(request, u'Left group')

