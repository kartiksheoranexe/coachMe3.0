from django.contrib import admin
from chat.models import Chat

# Register your models here.


class ChatAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'created_at']


admin.site.register(Chat, ChatAdmin),

