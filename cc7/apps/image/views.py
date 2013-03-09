# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from forms import UploadFileForm
from django.template import RequestContext

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print request.FILES
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')


    else:
        form = UploadFileForm()
        return render_to_response(
            'image/upload_form.html',
            {'form': form},
            context_instance=RequestContext(request)
        )
