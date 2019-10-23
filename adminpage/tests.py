from django.test import LiveServerTestCase
from selenium import webdriver
import time


class AdminLoginViewTest(LiveServerTestCase):
    browser = None

    @classmethod
    def setUpClass(cls):
        super(AdminLoginViewTest, cls).setUpClass()
        cls.browser = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(AdminLoginViewTest, cls).tearDownClass()

    def test_valid_login(self):
        self.browser.get('http://127.0.0.1:8000/a/login')
        inputUserName = self.browser.find_element_by_id('inputUsername')
        inputPassword = self.browser.find_element_by_id('inputPassword')
        loginnow = self.browser.find_element_by_id('loginnow')

        inputUserName.clear()
        inputUserName.send_keys('root')

        inputPassword.clear()
        inputPassword.send_keys('!root123')

        loginnow.click()
        time.sleep(2)