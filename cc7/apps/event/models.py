from django.db import models
from apps.account.models import Association

class Event(models.Model):
    title = models.CharField(max_length=255)
    organiser = models.ForeignKey(Association)
    description = models.TextField()
    place = models.CharField(max_length= 255)
    date = models.DateField()
    time = models.TimeField()
    
    def __unicode__(self):
        return unicode(self.title)
    
    def send_invitations(self, event):
        pass


