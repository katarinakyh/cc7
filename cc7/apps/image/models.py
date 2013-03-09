from django.db import models
from sorl.thumbnail import ImageField
from django.forms import ModelForm

class Image(models.Model):
    image = ImageField(upload_to='images')

    def __unicode__(self):
        return u'%s' %self.image

    def save(self, *args, **kwargs):
        super(Image, self).save(*args, **kwargs)

