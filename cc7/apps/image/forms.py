from django import forms
from models import Image

class UploadFileForm(forms.ModelForm):
    image = forms.FileField()
    class Meta:
        model = Image
