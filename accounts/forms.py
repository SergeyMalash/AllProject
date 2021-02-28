from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm

from accounts import tasks
from accounts.models import Account


class ChangeAccountForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')
    error_css_class = 'error'

    class Meta:
        model = Account
        fields = ('username', 'email', 'first_name', 'last_name')


class RegisterAccountForm(UserCreationForm):
    email = forms.EmailField(required=True, error_messages={})

    email.widget.attrs.update({'class': 'form-control mb-2'})

    class Meta(UserCreationForm.Meta):
        model = Account
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', )


class PasswordResetCustomForm(PasswordResetForm):
    """
    Форма для ввода адреса электронной почты для сброса пароля.
    """
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """Переопределённый метод отправки письма через Celery"""
        email = context['email']
        username = context['user'].username
        uid = context['uid']
        token = context['token']
        tasks.send_reset_password_email.delay(email, username, uid, token)
