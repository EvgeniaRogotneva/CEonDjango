import os, requests
import django, json
from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest, HttpResponse, QueryDict
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()


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
        self.client = Client()
        self.factory = RequestFactory()
        self.request = HttpRequest()

    def test_add_rate(self):
        request = HttpRequest()

        data = {
            "currency_code": "USD",
            "time": "2021-03-05 13:19:13+00:00",
            "rate": 1500
            }
        
        json_data = json.dumps(data)
        print('json', json_data)
        q = QueryDict(json_data, mutable=True)

        # data = 'currency_code=USD&time=2021-03-05 13:19:13+00:00&rate=150'
        # q = QueryDict(data, mutable=True)
        print(q)
        request.POST = q
        response = self.client.post(path='/add_rate', data=request.POST)
        print('headers',response.content)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/currencyexchange/')
        response = self.client.get('/get_rate_for_pair', {'from_currency_code': 'USD', 'to_currency_code': 'RUB',
                                                          'time': '2021-03-05 13:19:13+00:00'})
        print(response)

    def test_add_rate_by_api(self):
        data = {
            "currency_code": "USD",
            "time": "2021-03-05 13:19:13+00:00",
            "rate": 1500
        }
        response = self.client.post(path='/add_rate_by_api', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Rate has been added')

        data = {
            "from_currency_code": "USD",
            "to_currency_code": "RUB",
            "time": "2021-03-05 13:19:13+00:00",
        }

        response = self.client.post('/get_rate_for_pair', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print('response.content', response.content)
        self.assertEqual(response.content, b'we received your json')





