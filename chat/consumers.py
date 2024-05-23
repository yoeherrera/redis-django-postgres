from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import Message
from django.utils.timezone import now
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get('user')
        self.username = user.username if user and user.is_authenticated else 'Anonymous'

        # Join chat group
        self.chat_group_name = 'chat'
        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)

        await self.accept()

        # Send last 10 messages to the user
        await self.send_last_10_messages()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')

        if message:
            # Save message to database
            await self.save_message(message)

            # Send message to chat group
            await self.channel_layer.group_send(
                self.chat_group_name,
                {
                    'type': 'chat.message',
                    'message': message,
                    'username': self.username,
                }
            )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat.message',
            'message': message,
            'username': username,
        }))

    @database_sync_to_async
    def save_message(self, message):
        Message.objects.create(username=self.username, message=message)

    @database_sync_to_async
    def get_last_10_messages(self):
        messages = Message.objects.order_by('-timestamp')[:10]
        return [{'username': msg.username, 'message': msg.message} for msg in messages]

    async def send_last_10_messages(self):
        last_10_messages = await self.get_last_10_messages()
        await self.send(text_data=json.dumps({
            'type': 'last_10_messages',
            'messages': last_10_messages
        }))
