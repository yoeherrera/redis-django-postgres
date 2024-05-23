from django.test import TestCase
from chat.models import Message  # Import your Message model from your app

class MessageModelTest(TestCase):
    def test_message_creation(self):
        # Create a Message object with the required fields
        message = Message.objects.create(username="testuser", message="Hello, world!")

        # Perform assertions or further checks as needed
        self.assertEqual(message.username, "testuser")
        self.assertEqual(message.message, "Hello, world!")
        # Add more assertions as needed
