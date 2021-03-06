import os, requests
import django, json
from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest, HttpResponse, QueryDict


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from currencyexchange.views import erase_all
from django.contrib.auth.models import User
from currencyexchange.models import Key, Access, Resource
from currencyexchange.tests.test_auth import add_user_and_key_to_bd, remove_keys_and_users, add_permission


class UrlAvailableTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_add_rates(self):
        response = self.client.get('/add_rate')
        self.assertEqual(response.status_code, 200)

    def test_get_rate_for_pair(self):
        response = self.client.get('/get_rate_for_pair')
        self.assertEqual(response.status_code, 200)


class ClientRequestTestCase(TestCase):
    @classmethod
    def tearDownClass(cls):
        remove_keys_and_users()

    @classmethod
    def setUpTestData(cls):
        ivan = add_user_and_key_to_bd('IvanIvanov', 'Ivan', 'Ivanov', 'ivanMolodec', 'ivanov.ivan@mail.ru',
                               False, False, True, '07.08.2021')
        add_permission(id=ivan, access=Access.read, resource=Resource.rate)
        add_permission(id=ivan, access=Access.write, resource=Resource.rate)

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.request = HttpRequest()

    def test_add_and_get_rate_by_api(self):
        data = {
            "currency_code": "USD",
            "time": "2021-03-05 13:19:13+00:00",
            "rate": 1500
        }
        response = self.client.post(path='/api/add_rate_by_api', data=data, content_type='application/json',
                                    HTTP_API_USER_KEY="SXZhbkl2YW5vdg==")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"response": "Rate has been added"}')
        data = {
            "currency_code": "RUB",
            "time": "2021-03-05 13:19:13+00:00",
            "rate": 1
        }
        response = self.client.post(path='/api/add_rate_by_api', data=data, content_type='application/json',
                                    HTTP_API_USER_KEY="SXZhbkl2YW5vdg==")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"response": "Rate has been added"}')
        data = {
            "from_currency_code": "USD",
            "to_currency_code": "RUB",
            "time": "2021-03-05 13:19:13+00:00",
        }

        response = self.client.post('/api/get_rate_for_pair_by_api', data=data, content_type='application/json',
                                    HTTP_API_USER_KEY="SXZhbkl2YW5vdg==")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"response": "1 USD equals 1500.0 RUB"}')

    def test_send_wrong_request_to_api_get_rate(self):
        data = {
            "currency_code": "USD",
            "time": "2021-03-05 13:19:13+00:00",
            "rate": 1500
        }
        response = self.client.get(path='/api/add_rate_by_api', data=data, content_type='application/json',
                                   HTTP_API_USER_KEY="SXZhbkl2YW5vdg==")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'{"response": "I receive only POST request with json content type"}')

    def test_wrong_rate_for_add_rate_by_api(self):
        data = {
            "currency_code": "USD",
            "time": "2021-03-05 13:19:13+00:00",
            "rate": 0
        }
        response = self.client.post(path='/api/add_rate_by_api', data=data, content_type='application/json',
                                    HTTP_API_USER_KEY="SXZhbkl2YW5vdg==")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'{"rate": [{"message": "rate should be bigger than zero", "code": ""}]}')

    def test_erase_all_no_permission(self):
        response = self.client.get('/api/erase_all', HTTP_API_USER_KEY="SXZhbkl2YW5vdg==")
        print('response', response)
        self.assertEqual(response.status_code, 403)





