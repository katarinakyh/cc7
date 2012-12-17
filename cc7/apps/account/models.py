from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from django.db.models.signals import post_save
from django.dispatch import receiver

class MyProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')

    slug = models.SlugField(blank=True)
    description = models.TextField(blank=True)
    association = models.ManyToManyField('Association', blank=True, null=True)
    has_new_message = models.BooleanField(default=False)
    has_new_comment = models.BooleanField(default=False)
    
    def get_message(self):
        pass

    def get_user(self, request):
        user = User.objects.get(username=request.user)
        return user

    def send_message(self, to, text, thread):
        pass
    
    def send_message_to_group(self, to, text, thread):
        pass
    
    def comment(self, post, text):
        pass
    
    def __unicode__(self):
        return unicode(self.user)
    
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, **kwargs):
        MyProfile.objects.get_or_create(user=instance)
        
        
class Association(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='association')

    association = models.CharField(max_length=122)
    slug = models.SlugField()
    description = models.TextField()
    
    def __unicode__(self):
        return unicode(self.association)

    def remove_member(self, member):
        pass

    def remove_event(self, event):
        pass

    