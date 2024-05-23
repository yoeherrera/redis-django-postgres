from channels.testing import WebsocketCommunicator
from channels.db import database_sync_to_async
from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from chat.consumers import ChatConsumer
from chat.models import Message

class ChatConsumerTests(TransactionTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @staticmethod
    @database_sync_to_async
    def create_test_user(username, password):
        User = get_user_model()
        try:
            user = User.objects.create_user(username=username, password=password)
        except IntegrityError:
            user = User.objects.get(username=username)
        return user

    async def test_chat_consumer(self):
        # Ensure the user is properly awaited
        user = await self.create_test_user('testuser', 'password')

        # Instantiate the consumer with the authenticated user
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chat/$")
        communicator.scope['user'] = user

        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Receive initial messages (last 10 messages)
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'last_10_messages')

        # Send a message through the WebSocket
        await communicator.send_json_to({'message': 'Test message'})

        # Receive the message from the WebSocket
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'chat.message')
        self.assertEqual(response['message'], 'Test message')
        self.assertEqual(response['username'], 'testuser')

        # Check if the message is saved in the database
        messages = await database_sync_to_async(Message.objects.all)()
        messages_count = await database_sync_to_async(messages.count)()
        self.assertEqual(messages_count, 1)

        # Access the message synchronously
        message = await database_sync_to_async(messages.first)()
        self.assertEqual(message.username, 'testuser')
        self.assertEqual(message.message, 'Test message')

        # Clean up
        await communicator.disconnect()
