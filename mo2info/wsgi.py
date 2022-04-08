"""
WSGI config for mo2info project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import json
import os
import subprocess

from django.core.wsgi import get_wsgi_application

eb_env = json.loads(
    subprocess.run(
        "/opt/elasticbeanstalk/bin/get-config environment"
    ).stdout
)
for key, value in eb_env.items():
    os.environ.setdefault(key, value)

application = get_wsgi_application()
