# config/asgi.py

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Llama a django.setup() aquí, al principio
django.setup()

# Ahora que Django está configurado, podemos importar el resto
from apps.chat.middleware import TokenAuthMiddleware
import apps.chat.routing

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": TokenAuthMiddleware(
        URLRouter(
            apps.chat.routing.websocket_urlpatterns
        )
    ),
})