from django.contrib import admin
from models import Group, ActiveMember

class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class ActiveMemberAdmin(admin.ModelAdmin):
    pass

admin.site.register(Group,GroupAdmin)
admin.site.register(ActiveMember, ActiveMemberAdmin)