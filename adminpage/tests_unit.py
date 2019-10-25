from django.test import TestCase, Client
from django.contrib.auth.models import User
from adminpage.views import AdminLoginView
from codex.baseerror import PasswordError
import json


class UrlTest(TestCase):
    """test if url is reachable
    """
    def test_login_url(self):
        response = self.client.get('/a/login/')
        self.assertEqual(response.status_code, 200)

    def test_activity_list_url(self):
        response = self.client.get('/a/activity/list')
        self.assertEqual(response.status_code, 200)

    def test_acitivity_detail_url(self):
        response = self.client.get('/a/activity/detail?create=1')
        self.assertEqual(response.status_code, 200)

    def test_acitivity_menu_url(self):
        response = self.client.get('/a/activity/menu')
        self.assertEqual(response.status_code, 200)

    def test_activity_checkin_url(self):
        response = self.client.get('/a/activity/checkin')
        self.assertEqual(response.status_code, 200)


class AdminLoginTest(TestCase):
    """test admin login
    """
    def setUp(self):
        User.objects.create_superuser('root', 'root@test.com', '!root123')

    def test_login_url(self):
        """url test
        """
        c = Client()
        response = c.post('/api/a/login', {"username": "root", "password": "!root123"})
        self.assertEqual(response.status_code, 200)

    def test_valid_login(self):
        """invalid username & password
        """
        c = Client()
        response = c.post('/api/a/login', {"username": "root", "password": "!root123"})
        response_content = response.content.decode()
        response_content_dict = json.loads(response_content)
        self.assertEqual(response_content_dict['code'], 0)

    def test_valid_username(self):
        """invalid username
        """
        c = Client()
        response = c.post('/api/a/login', {"username": "weiyx", "password": "!root123"})
        response_content = response.content.decode()
        response_content_dict = json.loads(response_content)
        self.assertEqual(response_content_dict['code'], 7)

    def test_wrong_password(self):
        """wrong password
        """
        admin_login = AdminLoginView()
        admin_login.input = {}
        admin_login.input['username'] = 'root'
        admin_login.input['password'] = '123456'
        self.assertRaises(PasswordError, admin_login.post)
