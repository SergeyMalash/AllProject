from django.db import models

from accounts.models import Account


class Message(models.Model):
    message_text = models.CharField(verbose_name='Message text', max_length=300)
    user = models.ForeignKey(Account, verbose_name='User', on_delete=models.CASCADE, related_name='user_messages')
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    dialog = models.ForeignKey('Dialog', verbose_name='Chat', on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return f'Message from {self.user} at {self.created}'


class Dialog(models.Model):
    created = models.DateTimeField(verbose_name='Created date', auto_now_add=True)
    messages = models.ManyToManyField(Message, verbose_name='Messages', related_name='+', blank=True)
    users = models.ManyToManyField(Account, verbose_name='Users', related_name='dialogs')

    def __str__(self):
        return f'Chat between {self.talking_users()}'

    def talking_users(self):
        return ' and '.join(self.users.values_list('username', flat=True))
