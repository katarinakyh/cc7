from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm 
from userena.forms import EditProfileForm, SignupForm
from models import MyProfile
from django.contrib.auth.forms import PasswordChangeForm

attrs_dict = {'class': 'required'}
USERNAME_RE = r'^[\.e\w]+$'

class EditProfileFormExtra(EditProfileForm):
    class Meta:
        model = MyProfile
        exclude = ('user','slug','privacy','has_new_message','has_new_comment')
        
        
class SignupFormExtra(SignupForm):

    def clean_username(self):
        username  = self.cleaned_data['username']
        if len(username) < 2 :
            raise forms.ValidationError("Your username must be at least 2 characters long.")

        return username
    
    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) < 5 :
            raise forms.ValidationError("Password must be at least 5 characters long.")
        return password1

'''
class PasswordChangeFormExtra(PasswordChangeForm):

=======


class PasswordChangeFormExtra(PasswordChangeForm):
>>>>>>> b385ad3fbbf86656e1032854b8baab72f74f5afc
    def clean_new_password1(self):
        new_password1  = self.cleaned_data['new_password1']
        if len(new_password1) < 5 :
            raise forms.ValidationError("Password must be at least 5 characters long.")
<<<<<<< HEAD
        return new_password1
'''

