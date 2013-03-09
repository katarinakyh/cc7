from django.contrib import admin
from models import Image

from sorl.thumbnail.admin import AdminImageMixin

class ImageAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('pk','image', )

admin.site.register(Image,ImageAdmin)