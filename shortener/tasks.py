import datetime
from AllProject.celery import app
from django.core.mail import send_mail


@app.task()
def send_activation_notification(email):
    send_mail(
        'Subject here',
        'Here is the message.',
        None,
        [email],
        fail_silently=False,
    )
    print("Send E-mail complete!", datetime.datetime.now())
