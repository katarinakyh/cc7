from django.contrib import admin
from models import Place

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'description',  'latitude', 'longitude',  'date_created',)

admin.site.register(Place, PlaceAdmin)
