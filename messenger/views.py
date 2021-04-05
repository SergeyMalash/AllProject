from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from accounts.models import Account
from messenger.models import Dialog


class DialogListView(LoginRequiredMixin, ListView):
    template_name = 'messenger/dialog_list.html'

    def get_queryset(self):
        try:
            c = []
            for chat in Dialog.objects.filter(users=self.request.user):
                for user in chat.users.all():
                    c.append(user.username)
            result = set(c)
            result.remove(self.request.user.username)
        except KeyError:
            result = []
        return result


class DialogView(LoginRequiredMixin, ListView):
    template_name = 'messenger/dialog.html'
    chat = None

    def get(self, request, *args, **kwargs):
        if self.kwargs['username'] == self.request.user.username:
            return HttpResponseRedirect(reverse('search'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        user = get_object_or_404(Account, username=self.kwargs['username'])
        try:
            self.chat = Dialog.objects.filter(users=user).filter(users=self.request.user).prefetch_related('messages')[0]
        except (Dialog.DoesNotExist, IndexError):
            self.chat = Dialog.objects.create()
            self.chat.users.add(user, self.request.user)
        messages = {message.id: {'user': message.user.username, 'message_text': message.message_text} for message in
                    self.chat.messages.all().prefetch_related('user')}
        return messages

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['chat_id'] = self.chat.id if self.chat else None
        context['username'] = self.kwargs['username']
        return context
