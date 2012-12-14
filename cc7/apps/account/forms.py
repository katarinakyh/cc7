from userena.forms import EditProfileForm
from models import MyProfile


class EditProfileFormExtra(EditProfileForm):
    class Meta:
        model = MyProfile
        exclude = ('user','slug','privacy','has_new_message','has_new_comment')


