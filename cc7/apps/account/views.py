from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User
from models import Association
from apps.publication.forms import PostForm, CommentForm
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

        elif 'association_post' in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                form.save(commit = False)
                f = form
                f.title = "%s post" %pageuser.association
                f.author=profile
                f.association_page=pageuser
                f.is_public=True
                f.save()            
            else:
                print form.errors
        else:
            form = PostForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                f = form
                f.title = ' '
                f.author=profile
                f.is_public=False
                f.save()            
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
