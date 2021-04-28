import os, requests
import django, json
from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest, HttpResponse, QueryDict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from currencyexchange.views import erase_all

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

    def test_erase_all(self):
        response = self.client.get('/erase_all')
        self.assertEqual(response.status_code, 200)


class ClientRequestTestCase(TestCase):
    def setUp(self):
        erase_all(HttpRequest())
        self.client = Client()
        self.factory = RequestFactory()
        self.request = HttpRequest()

    def test_add_and_get_rate_by_api(self):
        data = {
            "currency_code": "USD",
            "time": "2021-03-05 13:19:13+00:00",
            "rate": 1500
        }
        response = self.client.post(path='/api/add_rate_by_api', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"response": "Rate has been added"}')
        data = {
            "currency_code": "RUB",
            "time": "2021-03-05 13:19:13+00:00",
            "rate": 1
        }
        response = self.client.post(path='/api/add_rate_by_api', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"response": "Rate has been added"}')
        data = {
            "from_currency_code": "USD",
            "to_currency_code": "RUB",
            "time": "2021-03-05 13:19:13+00:00",
        }

        response = self.client.post('/api/get_rate_for_pair_by_api', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"response": "1 USD equals 1500.0 RUB"}')

    def test_send_wrong_request_to_api_get_rate(self):
        data = {
            "currency_code": "USD",
            "time": "2021-03-05 13:19:13+00:00",
            "rate": 1500
        }
        response = self.client.get(path='/api/add_rate_by_api', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'{"response": "I receive only POST request with json content type"}')

    def test_wrong_rate_for_add_rate_by_api(self):
        data = {
            "currency_code": "USD",
            "time": "2021-03-05 13:19:13+00:00",
            "rate": 0
        }
        response = self.client.post(path='/api/add_rate_by_api', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'{"rate": [{"message": "rate should be bigger than zero", "code": ""}]}')

