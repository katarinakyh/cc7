from django.contrib import admin
from models import Comment, Message, Post


class CommentAdmin(admin.ModelAdmin):
    pass

class MessageAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    pass


admin.site.register(Comment,CommentAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Post,PostAdmin)
