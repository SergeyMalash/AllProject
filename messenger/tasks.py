import datetime

from django.core.mail import send_mail

from AllProject.celery import app


@app.task()
def send_activation_notification(email, token, username):
    send_mail(
        'Subject here',
        'http://127.0.0.1:8000/user/activation/' + username + '.' + token,
        None,
        [email],
        fail_silently=False,
    )
    print("Send E-mail complete!", datetime.datetime.now())
