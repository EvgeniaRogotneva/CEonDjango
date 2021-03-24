import os
import django
from django.test import TestCase, Client
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





