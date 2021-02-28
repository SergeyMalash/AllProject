Клонируйте репозиторий.
Удалите окончание `example` у файла `.env.prod.example` и в нём укажите следующее:
- логин и пароль от почты, которая будет использоваться для отправки писем.
- либо в качестве `DJANGO_EMAIL_BACKEND` укажите `django.core.mail.backends.console.EmailBackend` - в этом случае письма будут поступать в консоль DJANGO

Выполните команду `docker-compose -f docker-compose.prod.yaml up --build`

Проект будет работать на `127.0.0.1`