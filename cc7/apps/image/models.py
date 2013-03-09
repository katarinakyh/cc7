from django.db import models
from sorl.thumbnail import ImageField

class Image(models.Model):
    image = ImageField(upload_to='media/images')

    def __unicode__(self):
        return u'Comment to %s' %self.image

    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)

