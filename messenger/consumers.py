import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from messenger.models import Dialog, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope['user'].is_authenticated:
            self.chat_id = self.scope['url_route']['kwargs']['chat_id']
            self.room_group_name = 'chat_%s' % self.chat_id

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            print(self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message_to_db(self, message, user, chat_id):
        dialog = Dialog.objects.get(pk=chat_id)
        saved_message = Message.objects.create(user=user, message_text=message, dialog=dialog)
        dialog.messages.add(saved_message)
        return saved_message.id

    # Receive message from WebSocket
    async def receive(self, text_data, **kwargs):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        saved_message_id = await self.save_message_to_db(message, self.scope['user'], self.chat_id)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': self.scope['user'].username,
                'message_id': saved_message_id
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['user']
        message_id = event['message_id']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'message_id': message_id
        }))
