from django.contrib import admin
from models import Group, ActiveMember

class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class ActiveMemberAdmin(admin.ModelAdmin):
    list_display = ('pk', 'member', 'group', 'is_member')

admin.site.register(Group,GroupAdmin)
admin.site.register(ActiveMember, ActiveMemberAdmin)