# chat/test_consumers.py

from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from django.test import TestCase
from django.contrib.auth.models import User
from chat.consumers import ChatConsumer
from chat.models import Message
import json

class ChatConsumerTests(TestCase):
    async def test_chat_consumer(self):
        # Create a test user
        user = await self.create_test_user(username='testuser', password='password')

        # Instantiate the consumer
        communicator = WebsocketCommunicator(ChatConsumer, "/ws/chat/$")
        connected, _ = await communicator.connect()

        # Define the send function
        async def send(data):
            await communicator.send_json_to(data)

        # Test receiving a message
        await send({'message': 'Test message'})
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'chat.message')
        self.assertEqual(response['message'], 'Test message')
        self.assertEqual(response['username'], 'testuser')

        # Test database saving
        messages = await database_sync_to_async(Message.objects.all)()
        self.assertEqual(messages.count(), 1)
        self.assertEqual(messages[0].username, 'testuser')
        self.assertEqual(messages[0].message, 'Test message')

        # Clean up
        await communicator.disconnect()

    @staticmethod
    @database_sync_to_async
    def create_test_user(username, password):
        return User.objects.create_user(username=username, password=password)
