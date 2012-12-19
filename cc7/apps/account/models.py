from userena import settings as userena_settings
from easy_thumbnails.fields import ThumbnailerImageField
from userena.utils import get_gravatar
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile, upload_to_mugshot
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
        
        
class Association(models.Model):
    association = models.CharField(max_length=122)
    email = models.EmailField(help_text='admin contact for the association')
    slug = models.SlugField()
    description = models.TextField()
    MUGSHOT_SETTINGS = {'size': (userena_settings.USERENA_MUGSHOT_SIZE,
                                 userena_settings.USERENA_MUGSHOT_SIZE),
                        'crop': userena_settings.USERENA_MUGSHOT_CROP_TYPE}

    mugshot = ThumbnailerImageField(_('mugshot'),
                                    blank=True,
                                    upload_to=upload_to_mugshot,
                                    resize_source=MUGSHOT_SETTINGS,
                                    help_text=_('A personal image displayed in your profile.'))

    def get_mugshot_url(self):
        """
        Returns the image containing the mugshot for the user.

        The mugshot can be a uploaded image or a Gravatar.

        Gravatar functionality will only be used when
        ``USERENA_MUGSHOT_GRAVATAR`` is set to ``True``.

        :return:
            ``None`` when Gravatar is not used and no default image is supplied
            by ``USERENA_MUGSHOT_DEFAULT``.

        """
        # First check for a mugshot and if any return that.
        if self.mugshot:
            return self.mugshot.url

        # Use Gravatar if the user wants to.
        if userena_settings.USERENA_MUGSHOT_GRAVATAR:
            return get_gravatar(self.email,
                                userena_settings.USERENA_MUGSHOT_SIZE,
                                userena_settings.USERENA_MUGSHOT_DEFAULT)

        # Gravatar not used, check for a default image.
        else:
            if userena_settings.USERENA_MUGSHOT_DEFAULT not in ['404', 'mm',
                                                                'identicon',
                                                                'monsterid',
                                                                'wavatar']:
                return userena_settings.USERENA_MUGSHOT_DEFAULT
            else: return None



    def __unicode__(self):
        return unicode(self.association)

    def remove_member(self, member):
        pass

    def remove_event(self, event):
        pass

    