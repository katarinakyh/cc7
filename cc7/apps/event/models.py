from django.db import models
from django.utils.translation import ugettext as _
from apps.account.models import Association

class Event(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(_("Title"), max_length=255)
    organiser = models.ForeignKey(Association)
    description = models.TextField(_("Description"))
    place = models.CharField(_("Place"), max_length= 255)
    datetime_from = models.DateTimeField(_("From date and time"))
    datetime_to = models.DateTimeField(_("To date and time"))
    image = models.ImageField(upload_to='images/events/%Y/%m/%d', null=True, blank=True)

    def __unicode__(self):
        return unicode(self.title)
    
    def send_invitations(self, event):
        pass


