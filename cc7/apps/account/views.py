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
from apps.account.models import MyProfile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404

@login_required
def my_page(request, username):
    profile = request.user.get_profile()
    pageuser = get_object_or_404(User,username__iexact=username)
    pageprofile = pageuser.get_profile()
    associations = Association.objects.all()
    print pageprofile
    print profile
    
    if request.POST:
        if 'new_comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid():
                #print profile
                form.save(commit = False)
                f=form
                f.author=profile
                #print f.author
                f.post=request.POST['post']
                f.save()
            else:
                print form.errors

        else:
            form = PostForm(request.POST)
            if form.is_valid():
                form.save(commit = False)
                f = form
                f.title = 'no title'
                f.author=profile
                f.personal_page = profile
                f.is_public = False
                f.save()            
            else:
                print form.errors
                
    posts = Post.objects.filter(author = pageprofile).order_by('-date_created')
    post_form = PostForm()
    comment_form = CommentForm()
    return render_to_response('account/my_page.html',
                                   {'profile':profile,
                                    'pageprofile':pageprofile,
                                    'associations':associations,
                                    'posts':posts,
                                    'post_form':post_form,
                                    'comment_form':comment_form,
                                   },
                                  context_instance=RequestContext(request))   

class AssociationView(ListView):
    template_name = 'account/associations.html'
    model = Association
