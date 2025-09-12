# apps/chat/routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # La URL para la conexión WebSocket será algo como: ws://.../ws/chat/CITA_ID/
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]