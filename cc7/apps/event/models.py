from django.db import models
from django.utils.translation import ugettext as _
from apps.account.models import Association

class Event(models.Model):
    title = models.CharField(_("Title"), max_length=255)
    organiser = models.ForeignKey(Association)
    description = models.TextField(_("Description"))
    place = models.CharField(_("Place"), max_length= 255)
    date_from = models.DateField(_("From date"))
    time_from = models.TimeField(_("From time"))
    date_to = models.DateField(_("To date"))
    time_to = models.TimeField(_("To time"))

    def __unicode__(self):
        return unicode(self.title)
    
    def send_invitations(self, event):
        pass


