import os

from .base import *  # noqa: F401, F403

DEBUG = False

ALLOWED_HOSTS = [
    ".mo2.info",
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.mo2.info",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        # these env vars are managed by EB
        "NAME": os.environ["RDS_DB_NAME"],
        "USER": os.environ["RDS_USERNAME"],
        "PASSWORD": os.environ["RDS_PASSWORD"],
        "HOST": os.environ["RDS_HOSTNAME"],
        "PORT": os.environ["RDS_PORT"],
    }
}
