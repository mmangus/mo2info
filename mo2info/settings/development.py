import django_stubs_ext

from .base import *  # noqa: F401, F403

django_stubs_ext.monkeypatch()  # enable QuerySet generics


DEBUG = True

SECRET_KEY = "thisisthesecretkeyforlocaldevwhichisntthatsecretactually"

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mo2info",
        "USER": "postgres",
        "PASSWORD": "localdevpassword",
        "HOST": "postgres",
        "PORT": "5432",
    }
}
