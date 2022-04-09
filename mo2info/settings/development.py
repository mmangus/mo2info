from .base import *  # noqa: F401, F403

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
