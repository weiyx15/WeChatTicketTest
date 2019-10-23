from django.test import LiveServerTestCase
from selenium import webdriver
import time
import json


class FunctionTestWrapper(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()

    def tearDown(self) -> None:
        self.browser.quit()


class AdminLoginViewTest(FunctionTestWrapper):
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

        with open('admin_cookies.json', 'w') as f:
            json.dump(cookies, f)

    def test_invalid_username(self):
        self.browser.get('http://127.0.0.1:8000/a/login')
        inputUserName = self.browser.find_element_by_id('inputUsername')
        inputPassword = self.browser.find_element_by_id('inputPassword')
        loginnow = self.browser.find_element_by_id('loginnow')

        inputUserName.clear()
        inputUserName.send_keys('weiyx')

        inputPassword.clear()
        inputPassword.send_keys('!root123')

        loginnow.click()

        self.assertEqual(self.browser.find_element_by_id('alert').text, '用户名或密码错误')

    def test_wrong_password(self):
        self.browser.get('http://127.0.0.1:8000/a/login')
        inputUserName = self.browser.find_element_by_id('inputUsername')
        inputPassword = self.browser.find_element_by_id('inputPassword')
        loginnow = self.browser.find_element_by_id('loginnow')

        inputUserName.clear()
        inputUserName.send_keys('root')

        inputPassword.clear()
        inputPassword.send_keys('root')

        loginnow.click()

        self.assertEqual(self.browser.find_element_by_id('alert').text, '用户名或密码错误')


class ActivityListTest(FunctionTestWrapper):
    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        self.browser.delete_all_cookies()
        with open('admin_cookies.json', 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        for cookie in cookies:
            self.browser.add_cookie({
                'name': cookie['name'],
                'value': cookie['value']
            })

    def test_create_activity(self):
        self.browser.get('http://127.0.0.1:8000/a/activity/detail?create=1')
        time.sleep(1)

        inputName = self.browser.find_element_by_id('input-name')
        inputName.clear()
        inputName.send_keys('faust')
        time.sleep(1)

        inputKey = self.browser.find_element_by_id('input-key')
        inputKey.clear()
        inputKey.send_keys('faust')
        time.sleep(1)

        inputPlace = self.browser.find_element_by_id('input-place')
        inputPlace.clear()
        inputPlace.send_keys('assembly hall')
        time.sleep(1)

        inputDescription = self.browser.find_element_by_id('input-description')
        inputDescription.clear()
        inputDescription.send_keys('very good')
        time.sleep(1)

        inputPicUrl = self.browser.find_element_by_id('input-pic_url')
        inputPicUrl.clear()
        inputPicUrl.send_keys('''https://img-blog.csdnimg.cn/20190504232138969.PNG?x-oss-process=image/watermark,
        type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2RhX2thb19sYQ==,size_16,color_FFFFFF,t_70''')
        time.sleep(1)


