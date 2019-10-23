from django.test import LiveServerTestCase
from selenium import webdriver
import time
import json
from codex.baseerror import *


class AdminLoginViewTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()

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

        self.assertEqual(self.browser.title, '活动列表 - 紫荆之声')     # check if jump to activity list page

        cookies = self.browser.get_cookies()
        cookies = json.dumps(cookies)

        with open('admin_cookies.json', 'w') as f:
            f.write(cookies)

    def test_invalid_username(self):
        self.browser.get('http://127.0.0.1:8000/a/login')
        inputUserName = self.browser.find_element_by_id('inputUsername')
        inputPassword = self.browser.find_element_by_id('inputPassword')
        loginnow = self.browser.find_element_by_id('loginnow')

        inputUserName.clear()
        inputUserName.send_keys('weiyx')

        inputPassword.clear()
        inputPassword.send_keys('!root123')

        try:
            loginnow.click()
        except InputError:
            print('invalid input')

    def test_wrong_password(self):
        self.browser.get('http://127.0.0.1:8000/a/login')
        inputUserName = self.browser.find_element_by_id('inputUsername')
        inputPassword = self.browser.find_element_by_id('inputPassword')
        loginnow = self.browser.find_element_by_id('loginnow')

        inputUserName.clear()
        inputUserName.send_keys('root')

        inputPassword.clear()
        inputPassword.send_keys('root')

        try:
            loginnow.click()
        except PasswordError:
            print('wrong password')

