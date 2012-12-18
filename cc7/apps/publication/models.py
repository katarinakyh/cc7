from django.db import models
from apps.account.models import MyProfile, Association
from apps.event.models import Event

class Publication(models.Model):
    author = models.ForeignKey(MyProfile)
    date_created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()


class Post(Publication):
    title = models.CharField(max_length=50, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True)
    association = models.ForeignKey(Association, null=True, blank=True)    
    personal_page = models.ForeignKey(MyProfile, null=True, blank=True)
    is_public = models.BooleanField(default=True,)

    def __unicode__(self):
        return u'%s' %self.title
    
    def get_comments(self):
        pass


class Comment(Publication):
    post = models.ForeignKey(Post)
    
    def __unicode__(self):
        return u'Comment to %s' %self.post
    
    def comment(self):
        pass


class Message(Publication):
    title = models.CharField(max_length=50)
    to = models.ForeignKey(MyProfile)
    thread = models.IntegerField()

    def __unicode__(self):
        return u'%s' %self.title

    def get_recipient(self):
        pass

