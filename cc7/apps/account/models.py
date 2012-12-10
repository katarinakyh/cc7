from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile

class MyProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')

    slug = models.SlugField()
    description = models.TextField()
    association = models.ManyToManyField('Association')
    has_new_message = models.BooleanField(default=False)
    has_new_comment = models.BooleanField(default=False)
    
    def get_message(self):
        pass
    
    def send_message(self, to, text, thread):
        pass
    
    def send_message_to_group(self, to, text, thread):
        pass
    
    def comment(self, post, text):
        pass
    
    
class Association(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='association')

    slug = models.SlugField()
    description = models.TextField()
    
    def remove_member(self, member):
        pass

    def remove_event(self, event):
        pass

    