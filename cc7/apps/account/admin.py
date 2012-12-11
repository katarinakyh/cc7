from django.contrib import admin
from models import MyProfile, Association

class MyProfileAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("user",)}


class AssociationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("association",)}

admin.site.register('',MyProfileAdmin)
admin.site.register(Association, AssociationAdmin)