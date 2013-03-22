from django.db import models
from django.core.validators import MaxLengthValidator
from apps.account.models import MyProfile
from userena import settings as userena_settings
from easy_thumbnails.fields import ThumbnailerImageField
from userena.utils import get_gravatar
from django.utils.translation import ugettext as _
from userena.models import upload_to_mugshot
from django.db.models.signals import post_save
from django.dispatch import receiver


class MemberManager(models.Manager):

    def mygroups(self, request, group):
        profile = request.user.get_profile()
        mygroups = ActiveMember.objects.filter(member = profile, group = group)
        if(mygroups):
            is_member = True
        else:
            is_member = False
        return is_member


class Group(models.Model):
    title = models.CharField(max_length = 120)
    description = models.TextField(validators=[MaxLengthValidator(5000)],null=True, blank=True)
    initiator = models.ForeignKey(MyProfile, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(null=True, blank=True)
    MUGSHOT_SETTINGS = {'size': (userena_settings.USERENA_MUGSHOT_SIZE,
                                 userena_settings.USERENA_MUGSHOT_SIZE),
                        'crop': userena_settings.USERENA_MUGSHOT_CROP_TYPE}
    is_restricted = models.BooleanField(default=False, help_text="if the group is open or not, by default groups are open")

    mugshot = ThumbnailerImageField(_('mugshot'),
        blank=True,
        upload_to=upload_to_mugshot,
        resize_source=MUGSHOT_SETTINGS,
        help_text=_('Your group image, avatar.'))
    # TODO must have a default
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

    def get_active_members(self):
        active_group_members = ActiveMember.objects.filter(group = self.pk, is_member=True)
        return active_group_members

    def get_pending_members(self):
        pending_group_members = ActiveMember.objects.filter(group = self.pk, is_member=False)
        return pending_group_members

    def get_member(self, member):
        member = ActiveMember.objects.get(member = member)
        return member


    def __unicode__(self):
        return unicode(self.title)


# if member is in the list but not is_member member is pending
class ActiveMember(models.Model):
    member = models.ForeignKey(MyProfile)
    group = models.ForeignKey(Group, null=True, blank=True)
    is_member = models.BooleanField(default=False, help_text=_("If this user is a member or pending member."))

    objects = MemberManager()

    def __unicode__(self):
        return unicode('%s' % self.member).decode('utf8')
