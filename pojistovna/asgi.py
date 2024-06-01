"""
ASGI config for pojistovna project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pojistovna.settings')

application = get_asgi_application()
application = ProxyHeadersMiddleware(django_asgi_application, trusted_hosts=["your-render-app.onrender.com"])


