import os

from django.core.mail import send_mail
from django.template.loader import render_to_string

from AllProject.celery import app
from accounts.models import Account
from shortener.models import Tag


@app.task()
def send_activation_notification(email, token, username):
    context = {'token': token, 'username': username, 'site_host': os.getenv('SITE_HOST')}
    msg_plain = render_to_string('accounts/email/activation_letter_body.txt', context=context)
    msg_html = render_to_string('accounts/email/activation_letter_body.html', context=context)
    send_mail(
        'Подтверждение активации',
        msg_plain,
        None,
        [email],
        fail_silently=False,
        html_message=msg_html
    )


@app.task()
def create_base_tags(username):
    base_tags = ['Business', 'Work', 'Home', 'Family', 'IT', 'Hobby', 'Game', 'Book', 'Hot', 'Money']
    user = Account.objects.get(username=username)
    for tag in base_tags:
        t = Tag.objects.create(title=tag, user=user)
        t.save()


@app.task()
def send_reset_password_email(email, username, uid, token):
    context = {'uid': uid, 'token': token, 'username': username}
    msg_plain = render_to_string('accounts/email/reset_password_letter_body.txt', context=context)
    msg_html = render_to_string('accounts/email/reset_password_letter_body.html', context=context)
    send_mail(
        'Malash.ru - Сброс пароля',
        msg_plain,
        None,
        [email],
        fail_silently=False,
        html_message=msg_html
    )
