# apps/chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Se ejecuta cuando un usuario intenta conectarse.
        # Creamos un "grupo" de chat basado en el ID de la cita.
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Unirse al grupo de la sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Se ejecuta cuando un usuario se desconecta.
        # Abandonar el grupo de la sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recibir mensaje desde el WebSocket (desde el frontend)
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"] # Obtenemos el usuario autenticado

        # Enviar mensaje al grupo de la sala
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.first_name # Enviamos el nombre del usuario
            }
        )

    # Recibir mensaje desde el grupo de la sala y enviarlo al WebSocket (al frontend)
    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Enviar mensaje al WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))