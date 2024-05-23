from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth import get_user_model
from django.urls import reverse
from channels.db import database_sync_to_async
from django.test import Client  # Import Django Client

class ChatIntegrationTests(ChannelsLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.user = cls.create_test_user(username='testuser', password='password')
        cls.client = Client()  # Create a Client instance

    @staticmethod
    @database_sync_to_async
    def create_test_user(username, password):
        return get_user_model().objects.create_user(username=username, password=password)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_chat_integration(self):
        # Login using Django client
        login_data = {'username': 'testuser', 'password': 'password'}
        self.client.login(**login_data)

        # Navigate to chat page using client (follows redirects)
        response = self.client.get(reverse("chat:login_view"))
        self.assertEqual(response.status_code, 200)  # Assert successful login redirect

        # Use selenium for further interaction on the chat page

        # ... Rest of the test using selenium (unchanged from previous test)

        # Locate chat input and send message (unchanged)
        chat_input = WebDriverWait(self.selenium, 20).until(
            EC.presence_of_element_located((By.ID, 'chat-message-input'))
        )
        chat_input.send_keys('Hello, world!')
        chat_input.send_keys(Keys.RETURN)

        # Verify the message appears in the chat (unchanged)
        WebDriverWait(self.selenium, 10).until(
            EC.text_to_be_present_in_element((By.ID, 'chat-log'), 'Hello, world!')
        )
