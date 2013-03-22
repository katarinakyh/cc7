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
from forms import GroupPostForm, JoinGroupForm
from apps.account.models import MyProfile
from apps.publication.models import Post
from apps.publication.forms import CommentForm

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
        comment_form = CommentForm()
        join_group_form = JoinGroupForm()

        if (membership_active or membership_pending):
            can_request_membership = False
        else:
            can_request_membership = True
        form = GroupPostForm()
        group_post = Post.objects.filter(group=group_pk)
        context = {
            'group_object': group,
            'members': active_members,
            'pending': pending_members,
            'membership_active':membership_active,
            'membership_pending':membership_pending,
            'can_request_membership': can_request_membership,
            'user_id':user_id,
            'form': form,
            'group_post': group_post,
            'profile':user,
            'comment_form':comment_form,
            'join_group_form':join_group_form
        }
        context.update(kwargs)
        return super(GroupDetailView, self).get_context_data(**context)

    def post(self, request, *args, **kwargs):

        # if comment post
        if 'new_comment' in request.POST:
            author = request.POST.get('author')
            author = MyProfile.objects.get(pk=author)
            post = request.POST.get('post')
            post = Post.objects.get(pk=post)
            body = request.POST.get('body')
            form = CommentForm()
            form.instance.author = author
            form.instance.post = post
            form.instance.body = body

        # if user ask to join group
        elif 'join_group' in request.POST:
            user = request.POST.get('user')
            user = MyProfile.objects.get(pk=user)
            group = request.POST.get('group')
            group = Group.objects.get(pk=group)
            membership = ActiveMember.objects.get(group=group, member = user)

            # if you are in the group and the group is open - redirect
            if user == membership.member and group.is_restricted == False:
                return HttpResponseRedirect( request.path )

            form = JoinGroupForm()
            form.instance.member = user
            form.instance.group = group
            if group.is_restricted == True:
                form.instance.is_member = 0
            else:
                form.instance.is_member = 1

        # if a pending user is granted membership
        elif 'add_pending' in request.POST:
            user = request.POST.get('user')
            user = MyProfile.objects.get(pk=user)
            group = request.POST.get('group')
            group = Group.objects.get(pk=group)
            membership = ActiveMember.objects.get(member = user, group = group)
            if membership.is_member == False:
                membership.is_member = True
            else:
                membership.is_member = False
            membership.save()
            return HttpResponseRedirect( request.path )

        # if user is posting a post in group
        elif 'new_post' in request.POST:
            author = request.POST.get('author')
            author = MyProfile.objects.get(pk=author)
            group = request.POST.get('group')
            group = Group.objects.get(pk=group)
            body = request.POST.get('body')
            form = GroupPostForm()
            form.instance.author = author
            form.instance.group = group
            form.instance.body = body
            form.instance.is_public = False

        else:
            return HttpResponseRedirect( request.path )

        form.cleaned_data = True # TODO this is very bad make a real clean
        form.save()
        return HttpResponseRedirect( request.path )

class GroupCreateView(CreateView):
    template_name = 'group/create_group.html'
    model = Group
    success_url = '/group/'
    form_class = GroupForm

    def form_valid(self, form):
        form.instance.inititator = self.request.user.get_profile()
        form.instance.title = self.request.POST.get('title')
        form.save()

        # make the initiator of the group member of the group
        group = Group.objects.get(pk=form.instance.pk)
        user = self.request.user.get_profile()
        new_member = ActiveMember(member=user)
        new_member.group = group
        new_member.is_member = True
        new_member.save()
        return HttpResponseRedirect( self.success_url )


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

