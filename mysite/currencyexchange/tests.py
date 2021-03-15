import os
import django
from django.test import TestCase
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from .models import TimeAndCourse


class SetTestCase(TestCase):

    def setUp(self):
        TimeAndCourse.objects.create(currency_code='RUB', time=datetime.now(), rate=1)
        TimeAndCourse.objects.create(currency_code='USD', time=datetime.now(), rate=70)
        TimeAndCourse.objects.create(currency_code='USD', time=datetime.now(), rate=80)
        TimeAndCourse.objects.create(currency_code='EUR', time=datetime.now(), rate=90)


    def tearDown(self) -> None:
        TimeAndCourse.objects.all().delete()

    def test_get_currency(self):
        rub = TimeAndCourse.objects.get(currency_code="RUB")
        usd = TimeAndCourse.objects.get(currency_code="USD")
        self.assertEqual(rub.currency_code, 'RUB')
        self.assertEqual(usd.currency_code, 'USD')

    def test_get_rate_for_pair(self):
        print(TimeAndCourse.objects.filter(currency_code='USD').exclude(rate__lt=75))



