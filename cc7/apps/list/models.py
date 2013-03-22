from django.db import models
from django.core.validators import MaxLengthValidator
from apps.account.models import MyProfile
from django.utils.translation import ugettext as _


class ItemList(models.Model):
    title = models.CharField(max_length = 120)
    description = models.TextField(validators=[MaxLengthValidator(5000)], null=True, blank=True)
    initiator = models.ForeignKey(MyProfile, null=True, blank=True)
    image = models.ImageField(upload_to = 'listimages/',null=True, blank=True)
    is_restricted = models.BooleanField(default=True, help_text="restricted")

    def __unicode__(self):
        return unicode('%s' %self.title)

class ListItemManager(models.Manager):

    def get_list_url(self):
        print "inside list_url"
        print self
        url = 'list/2'
        return url

class ListItem(models.Model):
    item_list = models.ForeignKey(ItemList)
    title = models.CharField(max_length = 120)
    description = models.TextField(validators=[MaxLengthValidator(5000)],null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now = True)
    order = models.PositiveSmallIntegerField(null=True, blank=True)

    objects = ListItemManager()

    class Meta:
        ordering=['date_modified']

    def __unicode__(self):
        return unicode('%s' % self.title)

    def get_list_item_for_list(self):
        list_item = ListItem.objects.filter(item_list = self.pk)
        return list_item


    def get_active_members(self):
        active_group_members = ListMember.objects.filter(group = self.pk, is_member=True)
        return active_group_members

    def get_pending_members(self):
        pending_group_members = ListMember.objects.filter(group = self.pk, is_member=False)
        return pending_group_members

    def get_member(self, member):
        member = ListMember.objects.get(member = member)
        return member

class ListMember(models.Model):
    member = models.ForeignKey(MyProfile)
    list = models.ForeignKey(ItemList, null=True, blank=True)
    is_member = models.BooleanField(default=False, help_text=_("If this user is a member."))
    key = models.FloatField()

    def __unicode__(self):
        return unicode('%s' % self.member).decode('utf8')
