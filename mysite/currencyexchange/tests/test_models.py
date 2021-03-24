import os
import django
from django.test import TestCase, Client
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from currencyexchange.models import TimeAndCourse
from currencyexchange.views import erase_all


class FieldsTestCase(TestCase):

    def setUp(self) -> None:
        TimeAndCourse.objects.create(currency_code='RUB', time=datetime.now(), rate=1)
        TimeAndCourse.objects.create(currency_code='USD', time=datetime.now(), rate=70)
        TimeAndCourse.objects.create(currency_code='EUR', time=datetime.now(), rate=90)

    def tearDown(self) -> None:
        TimeAndCourse.objects.all().delete()

    def test_get_rate_for_pair(self):
        rate = TimeAndCourse.objects.values()
        print(rate)


