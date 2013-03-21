from django.db import models
from django.core.validators import MaxLengthValidator
from apps.account.models import MyProfile, Association
from apps.event.models import Event
from apps.map.models import Place
from apps.image.models import Image
from apps.group.models import Group

POST_TYPE = (
    ('1', 'Post'),
    ('2', 'Event'),
    ('3', 'Accociation'),
    ('4', 'Group'),
    ('5', 'List'),
    ('6', 'Meeting'),
)

class Post(models.Model):
    author = models.ForeignKey(MyProfile, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(validators=[MaxLengthValidator(10000)])
    title = models.CharField(max_length=50, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, blank=True)
    association = models.ForeignKey(Association, null=True, blank=True)
    group = models.ForeignKey(Group, null=True, blank=True)
    # list = models.ForeignKey(ItemList, null=True, blank=True)
    # posted_type = models.IntegerField(choices=POST_TYPE, null=True, blank=True)

    place = models.ForeignKey(Place, null=True, blank=True)
    is_public = models.BooleanField(default=True, help_text="publish on stream")

    image = models.ImageField(upload_to='images/posts/%Y/%m/%d', null=True, blank=True)

    """
    image = model.ForeignKey(Image, null=True, blank=True)
    date_changed = models.DateTimeField(auto_now = True)
    type = models.CharField(max_length=20, choices = POST_TYPE)
    """

    def __unicode__(self):
        return u'%s' %self.title
    
    def get_comments(self):
        pass


class Comment(models.Model):
    author = models.ForeignKey(MyProfile)
    date_created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(validators=[MaxLengthValidator(5000)])
    post = models.ForeignKey(Post, default=1, null=True,blank=True)
    event = models.ForeignKey(Event,default=1, null=True, blank=True)

    def __unicode__(self):
        return u'Comment to %s' %self.post
    
    def comment(self):
        pass


class Message(models.Model):
    author = models.ForeignKey(MyProfile, related_name="author")
    date_created = models.DateTimeField(auto_now_add=True)
    body = models.TextField(validators=[MaxLengthValidator(5000)])
    title = models.CharField(max_length=50)
    to = models.ForeignKey(MyProfile)
    thread = models.IntegerField()
    #is_read = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' %self.title

    def get_recipient(self):
        pass
