# Установка

Клонируйте репозиторий.

Выполните `chmod +x entrypoint.sh`

Выполните команду `docker-compose -f docker-compose.example.yaml up --build`

Затем `docker-compose -f docker-compose.example.yaml exec django bash`

Затем `celery -A AllProject worker -l INFO` - эта команда запустит Celery

Проект будет работать на `127.0.0.1`

# AllProject

Без авторизации доступны возможности сокрашать ссылки (с QR-кодом) и анонимного чата (`127.0.0.1/anonymous/`).

После авторизации можно:
- задавать свой суффикс для ссылки (а не случайный), редактировать ссылки, добавлять ссылкам теги
- вести переписку с другими зарегистрированными пользователями

Оба чата сделаны через WebSocket.

Анонимный чат сделан на VUE в одном файле (просто пощупал VUE и JS)

Письма (регистрация и сброс пароля) отправляются через Celery
