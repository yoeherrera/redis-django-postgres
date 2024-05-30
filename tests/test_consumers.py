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
        # Create a test user
        user = await self.create_test_user('testuser', 'password')

        # Instantiate the consumer with the authenticated user
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chat/")
        communicator.scope['user'] = user

        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Send a message through the WebSocket
        await communicator.send_json_to({'type': 'chat.message', 'message': 'Test message', 'username': 'testuser'})

        # Receive the message from the WebSocket
        try:
            response = await communicator.receive_json_from(timeout=5)  # Adjust timeout value as needed
            self.assertIn('message', response)  # Check if 'message' key exists in the response
            self.assertIn('username', response)  # Check if 'username' key exists in the response
        except KeyError as e:
            self.fail(f"Response does not contain expected keys: {e}. Response: {response}")

        # Clean up
        await communicator.disconnect()
