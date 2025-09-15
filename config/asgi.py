# config/asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

# Esta línea debe estar aquí
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Y esta línea debe estar justo después, ANTES de los otros imports
django.setup()

# Ahora que Django está configurado, es seguro importar el resto
from channels.auth import AuthMiddlewareStack
from apps.chat.middleware import TokenAuthMiddleware
import apps.chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        TokenAuthMiddleware(
            URLRouter(
                apps.chat.routing.websocket_urlpatterns
            )
        )
    ),
})