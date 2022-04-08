# This is the production Dockerfile; see `dev/Dockerfile` for the one
#  that powers the dev environment
FROM python:3.10

WORKDIR /mo2info
EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=mo2info.settings.production

# install postgres 14 client
RUN apt-get update
RUN apt-get install -y lsb-release
RUN echo \
    "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main"\
     > /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add  -
RUN apt-get update
RUN apt-get install -y postgresql-14

# install build deps
RUN pip3 install --upgrade pip
RUN pip3 install pip-tools

COPY . /mo2info
RUN pip-sync

RUN python manage.py migrate

ENTRYPOINT gunicorn --bind :8000 --workers 5 portfolio.wsgi:application
