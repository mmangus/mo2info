# this is the Dockerfile for the dev environment, not executed on EB
FROM python:3.10

WORKDIR /mo2info
EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=mo2info.settings.development
ENV PGPASSFILE=/mo2info/.pgpass

COPY /dev/.pgpass /mo2info/.pgpass
RUN chmod 0600 /mo2info/.pgpass

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

# install project requirements
# even though we have a volume, we want to bust cache if these change
COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt
RUN pip-sync requirements.txt requirements-dev.txt

RUN createdb mo2info

ENTRYPOINT python manage.py runserver 0.0.0.0:8000
