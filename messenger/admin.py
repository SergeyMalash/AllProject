from django.contrib import admin

from messenger.models import Message, Dialog


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    model = Message
    list_display = ('created', 'user', 'message_text', 'dialog')


@admin.register(Dialog)
class ChatAdmin(admin.ModelAdmin):
    model = Dialog
    list_display = ('created', 'talking_users')
