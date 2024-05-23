# chat/tests_integration.py

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class ChatIntegrationTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_chat_integration(self):
        self.selenium.get(f'{self.live_server_url}/chat/login/')
        username_input = self.selenium.find_element_by_name('username')
        username_input.send_keys('testuser')
        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys('password')
        password_input.send_keys(Keys.RETURN)
        time.sleep(1)  # Wait for login redirect

        # Send a message
        message_input = self.selenium.find_element_by_id('chat-message-input')
        message_input.send_keys('Test message')
        message_input.send_keys(Keys.RETURN)
        time.sleep(1)  # Wait for message to be sent

        # Check if message is displayed
        messages = self.selenium.find_elements_by_css_selector('.message')
        self.assertEqual(len(messages), 1)
        self.assertIn('Test message', messages[0].text)
