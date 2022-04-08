from .base import *

DEBUG = True

SECRET_KEY = "thisisthesecretkeyforlocaldevwhichisntthatsecretactually"

ALLOWED_HOSTS = ["localhost", ]

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mo2info",
        "USER": "postgres",
        "PASSWORD": "localdevpassword",
        "HOST": "postgres",
        "PORT": "5432",
    }
}
