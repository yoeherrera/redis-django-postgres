from channels.testing import ChannelsLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth import get_user_model
from django.urls import reverse
from channels.db import database_sync_to_async
from django.test import Client

class ChatIntegrationTests(ChannelsLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)  # Set implicit wait to handle element presence
        cls.user = cls.create_test_user(username='postgres', password='postgres')
        cls.client = Client()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    @staticmethod
    @database_sync_to_async
    def create_test_user(username, password):
        return get_user_model().objects.create_user(username=username, password=password)

    def login(self):
        # Login using Django client
        login_data = {'username': 'testuser', 'password': 'password'}  # Use your test user credentials
        self.client.login(**login_data)

        # Navigate to chat page using client (follows redirects)
        response = self.client.get(reverse("chat:login_view"))
        self.assertEqual(response.status_code, 200)  # Assert successful login redirect

    def test_chat_integration(self):
        # Perform login
        self.login()

        # Use selenium for further interaction on the chat page
        self.selenium.get(self.live_server_url + reverse('chat:login_view'))  # Navigate to chat page

        # Locate chat input and send message
        chat_input = self.selenium.find_element(By.ID, 'chat-message-input')
        chat_input.send_keys('Hello, world!')
        chat_input.send_keys(Keys.RETURN)

        # Verify the message appears in the chat
        chat_log = WebDriverWait(self.selenium, 30).until(
            EC.text_to_be_present_in_element((By.ID, 'chat-log'), 'Hello, world!')
        )
        self.assertTrue(chat_log)  # Assert that message is present in the chat log
