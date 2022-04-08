import os

from .base import *

DEBUG = False

ALLOWED_HOSTS = ["michaelmang.us", ]

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        # these env vars are managed by EB
        "NAME": os.environ["RDS_DB_NAME"],
        "USER": os.environ["RDS_USERNAME"],
        "PASSWORD": os.environ["RDS_PASSWORD"],
        "HOST": os.environ["RDS_HOST"],
        "PORT": os.environ["RDS_PORT"],
    }
}
