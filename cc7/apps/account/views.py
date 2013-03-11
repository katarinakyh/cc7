from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, RedirectView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from models import Association
from apps.publication.forms import PostForm, CommentForm, ThreadForm
from apps.publication.models import Post
from apps.event.models import Event
from apps.account.models import MyProfile                                                             
from apps.stream.views import save_comment
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from itertools import chain
from operator import attrgetter

@login_required
def my_page(request, *args, **kwargs):
    
    profile = request.user.get_profile()
    associations = Association.objects.all()
    
    for key in kwargs:
        model = key
        key = kwargs[key]
        
    if model == 'username':
        pageuser = get_object_or_404(User,username__iexact=key)
        pageprofile = pageuser.get_profile()
    elif model == 'association':
        pageuser = get_object_or_404(Association,slug__iexact=key)
        pageprofile = pageuser
    
    if request.POST:
        if 'new_comment' in request.POST:
            save_comment(request, profile)
            if model == 'username':
                return HttpResponseRedirect(reverse('my_page', args=(pageuser.username,)))
            else:
                return HttpResponseRedirect(reverse('show_association', args=(pageprofile.slug,)))

        elif 'association' in request.POST:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(commit = False)
                title =  request.POST.get('title')
                if title:
                    pass
                else:
                    form.instance.title = ">>"
                form.instance.author = profile
                form.instance.association = pageuser
                form.instance.is_public = True
                form.save()
                return HttpResponseRedirect(reverse('show_association', args=(pageprofile.slug,)))
            else:
                print form.errors
        else:
            form = PostForm(request.POST, request.FILES)
            print request.FILES.get('image')
            if form.is_valid():
                form.save(commit=False)
                title = request.POST.get('title')
                if title:
                    pass
                else:
                    form.instance.title = ">>"
                form.instance.author = profile
                form.instance.is_public = False
                form.save()            
                return HttpResponseRedirect(reverse('my_page', args=(pageuser.username,)))
            else:
                print form.errors
                
    can_edit = False
    is_association = False
    
    if model == 'username':
        object_list = Post.objects.defer('event','association').filter(author = pageprofile).order_by('-date_created')
        template = 'account/my_page.html'
    elif model == 'association':
        posts = Post.objects.filter(is_public=True, association = pageprofile).order_by('-date_created')
        events = Event.objects.filter(organiser = pageprofile).order_by('-date_created')
        object_list =  sorted(chain(posts, events), key=attrgetter('date_created'))

        for a in profile.association.all():
            if pageuser == a:
                can_edit = True
        template = 'account/my_association.html'
        is_association=True
        
    post_form = PostForm()
    comment_form = CommentForm()

    return render_to_response(template,
                                   {'profile':profile,
                                    'pageprofile':pageprofile,
                                    'associations':associations,
                                    'object_list':object_list,
                                    'post_form':post_form,
                                    'comment_form':comment_form,
                                    'can_edit': can_edit,
                                    'is_association': is_association,
                                   },
                                  context_instance=RequestContext(request))

class AssociationView(ListView):
    template_name = 'account/associations.html'
    model = Association


class AssociationActivityBase(RedirectView):
    def get(self, request, *args, **kwargs):
        association = Association.objects.get(slug=kwargs.get('slug'))
        self.update_action(request, association, request.user.get_profile())
        success_url = request.META.get('referer') or '/'

        print 'groups', request.user.get_profile().association.all()
        return HttpResponseRedirect(success_url)

class AssociationJoinView(AssociationActivityBase):
    """
    Lets a user join an Association (group)
    """
    def update_action(self, request, association, user_profile):
        if association not in user_profile.association.all():
            user_profile.association.add(association)
            user_profile.save()
            messages.success(request, u'Joined group')

class AssociationLeaveView(AssociationActivityBase):
    """
    Lets a user leave an Association (group)
    """
    def update_action(self, request, association, user_profile):
        if association in user_profile.association.all():
            user_profile.association.remove(association)
            user_profile.save()
            messages.success(request, u'Left group')
