from django import forms
from django.utils.translation import ugettext_lazy as _
from userena.forms import EditProfileForm, SignupForm
from models import MyProfile


class EditProfileFormExtra(EditProfileForm):
    class Meta:
        model = MyProfile
        exclude = ('user','slug','privacy','has_new_message','has_new_comment')
        
USERNAME_RE = r'^[a-zA-Z]+$'
attrs_dict = {'class': 'required'}

class SignupFormExtra(SignupForm):
    """
    Form for creating a new user account.

    Validates that the requested username and e-mail is not already in use.
    Also requires the password to be entered twice and the Terms of Service to
    be accepted.

    """
    username = forms.RegexField(regex=USERNAME_RE,
                                min_length=5,
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _('Username must contain only letters, numbers, dots and underscores.')})
    password1 = forms.CharField(min_length=5, widget=forms.PasswordInput(attrs=attrs_dict,
                                                           render_value=False),
                                label=_("Create password"))
    password2 = forms.CharField(min_length=5, widget=forms.PasswordInput(attrs=attrs_dict,
                                                           render_value=False),
                                label=_("Repeat password"))
