FROM python:3.7.9-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt update
RUN apt install postgresql -y
RUN apt install gcc -y
RUN apt install python3-dev -y
RUN apt install musl-dev -y
RUN apt install netcat -y
RUN apt install libpq-dev -y

# lint
RUN pip install --upgrade pip
COPY . .
COPY requirements.txt .
# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN groupadd app
RUN useradd -m -g app app -p PASSWORD
RUN usermod -aG app app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/django
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
COPY . $APP_HOME
WORKDIR $APP_HOME

RUN pip install -r requirements.txt

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

ENTRYPOINT ["/home/app/django/entrypoint.sh"]