from django.contrib import admin
from models import ItemList, ListItem, ListMember

class ItemListAdmin(admin.ModelAdmin):
    pass

class ListItemAdmin(admin.ModelAdmin):
    pass

class ListMemberAdmin(admin.ModelAdmin):
    pass

admin.site.register(ItemList,ItemListAdmin)
admin.site.register(ListItem, ListItemAdmin)
admin.site.register(ListMember, ListMemberAdmin)