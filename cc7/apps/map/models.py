from django.db import models
from django.core.validators import MaxLengthValidator



class Place(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(validators=[MaxLengthValidator(1000)], null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    map_json = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    