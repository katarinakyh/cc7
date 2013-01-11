from django import forms
from django.utils.translation import ugettext_lazy as _
from userena.forms import EditProfileForm, SignupForm
from models import MyProfile
from django.contrib.auth.forms import PasswordChangeForm

attrs_dict = {'class': 'required'}

class EditProfileFormExtra(EditProfileForm):
    class Meta:
        model = MyProfile
        exclude = ('user','slug','privacy','has_new_message','has_new_comment')
        
USERNAME_RE = r'^[\.e\w]+$'


class SignupFormExtra(SignupForm):
    """
    Form for creating a new user account.

    Validates that the requested username and e-mail is not already in use.
    Also requires the password to be entered twice and the Terms of Service to
    be accepted.

    """
    username = forms.RegexField(regex=USERNAME_RE,
                                min_length=3,
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _('Username must contain only leDDers, numbers, dots and underscores.')})
    
    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        if len(password1) < 5 :
            raise forms.ValidationError("Password must be at least 5 characters long.")
        return password1
'''
class PasswordChangeFormExtra(PasswordChangeForm):

    def clean_new_password1(self):
        new_password1  = self.cleaned_data['new_password1']
        if len(new_password1) < 5 :
            raise forms.ValidationError("Password must be at least 5 characters long.")
        return new_password1
'''
