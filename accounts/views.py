from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, \
    PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView, DeleteView

from accounts import tasks
from accounts.forms import RegisterAccountForm, ChangeAccountForm, PasswordResetCustomForm
from accounts.models import Account


class DetailAccount(LoginRequiredMixin, TemplateView):
    """Главная страница профиля"""
    template_name = 'accounts/detail_account.html'
    model = Account
    
    def get_context_data(self, **kwargs):
        return super(DetailAccount, self).get_context_data(**kwargs)


class RegisterAccountView(CreateView):
    """Страница с формой для регистрации"""
    model = Account
    template_name = 'accounts/register_account.html'
    form_class = RegisterAccountForm
    success_url = reverse_lazy('register_done')
    object = None

    def form_valid(self, form):
        self.object = form.save()
        activation_token = PasswordResetTokenGenerator()
        token = activation_token.make_token(self.object)
        tasks.send_activation_notification.delay(form.cleaned_data['email'], token, self.object.username)
        return HttpResponseRedirect(self.get_success_url())


class RegisterAccountDoneView(TemplateView):
    """Страница после успешной регистрации"""
    template_name = 'accounts/register_done.html'


class ActivationAccountView(DetailView):

    def get_object(self, queryset=None):
        username = self.kwargs['username']
        token = self.kwargs['token']
        try:
            user = Account.objects.get(username=username)
        except Account.DoesNotExist:
            raise Http404('user not found')
        activation_token = PasswordResetTokenGenerator()
        if user.is_active:
            self.template_name = 'accounts/account_is_activated.html'
        elif activation_token.check_token(user, token):
            self.template_name = 'accounts/activation_done.html'
            user.is_active = True
            tasks.create_base_tags.delay(username)
            user.save()
        else:
            self.template_name = 'accounts/activation_fail.html'
        return user


class LoginAccountView(LoginView):
    """Страница входа"""
    template_name = 'accounts/login_account.html'


class LogoutAccountView(LogoutView):
    """Страница для выхода из авторизованой зоны"""
    template_name = 'accounts/logout_account.html'


class ChangeAccountView(LoginRequiredMixin, UpdateView):
    """Страница смены личных данных"""
    template_name = 'accounts/change_account.html'
    model = Account
    form_class = ChangeAccountForm
    success_url = reverse_lazy('detail_account')

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.request.user.pk)


class DeleteAccountView(LoginRequiredMixin, DeleteView):
    """Страница удаления профиля"""
    model = Account
    template_name = 'accounts/delete_account.html'
    success_url = reverse_lazy('index')
    object = None

    def get_object(self, queryset=None):
        obj = Account.objects.get(pk=self.request.user.pk)
        return obj

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.success_url)


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    """Страница смены пароля"""
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('password_reset_complete')


class ResetPasswordView(PasswordResetView):
    """Страница сброса пароля с помощью почты"""
    success_url = reverse_lazy('password_reset_done')
    template_name = 'accounts/reset_password.html'
    email_template_name = 'accounts/email/reset_password_email.html'
    subject_template_name = 'accounts/email/reset_password_subject.txt'
    form_class = PasswordResetCustomForm
    

class ResetPasswordDoneView(PasswordResetDoneView):
    template_name = 'accounts/reset_password_done.html'


class ResetPasswordConfirmView(PasswordResetConfirmView):
    """Страница для указания пароля после сброса"""
    template_name = 'accounts/reset_password_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class ResetPasswordCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/reset_password_complete.html'
