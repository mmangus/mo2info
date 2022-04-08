"""
ASGI config for mo2info project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""
from django.core.asgi import get_asgi_application

from .set_environment import set_environment

set_environment()

application = get_asgi_application()
