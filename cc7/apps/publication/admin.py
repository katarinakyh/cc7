from django.contrib import admin
from models import Comment, Message, Post

class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk','author', 'date_created',)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'to', 'date_created',)
    
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'body',  'author', 'image', 'date_created',)

admin.site.register(Comment,CommentAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Post,PostAdmin)


