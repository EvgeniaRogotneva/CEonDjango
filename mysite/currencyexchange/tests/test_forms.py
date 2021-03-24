import os
import django
from django.test import TestCase, Client
from datetime import datetime, timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from currencyexchange.forms import AddRate, GetRate


class FormTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_future_date_add_rate(self):
        data = {'currency_code': 'USD', 'time': datetime.now() + timedelta(days=30), 'rate': 30}
        answer = AddRate(data)
        self.assertEqual(answer.is_valid(), False)

    def test_future_date_get_rate(self):
        data = {'from_currency_code': 'USD', 'to_currency_code': 'EUR', 'time': datetime.now() + timedelta(days=30)}
        answer = GetRate(data)
        self.assertEqual(answer.is_valid(), False)

    def test_zero_rate_add_rate(self):
        data = {'currency_code': 'USD', 'time': datetime.now(), 'rate': 0}
        answer = AddRate(data)
        self.assertEqual(answer.is_valid(), False)

    def test_negative_rate_add_rate(self):
        data = {'currency_code': 'USD', 'time': datetime.now(), 'rate': -15}
        answer = AddRate(data)
        self.assertEqual(answer.is_valid(), False)

    def test_get_pair_with_different_date(self):
        data = {'currency_code': 'USD', 'time': '2021-03-05 13:19:13+00:00', 'rate': 75}
        answer = AddRate(data)
        self.assertEqual(answer.is_valid(), True)
        data = {'currency_code': 'RUB', 'time': '2021-03-09 13:19:13+00:00', 'rate': 1}
        answer = AddRate(data)
        self.assertEqual(answer.is_valid(), True)
        data = {'from_currency_code': 'USD', 'to_currency_code': 'RUB', 'time': datetime.fromisoformat('2021-03-09 13:19:13+00:00')}
        answer = GetRate(data)
        print(answer)
        self.assertEqual(answer.is_valid(), True)


