import os, requests
import django, json
from django.test import TestCase, Client
from django.http import HttpRequest, HttpResponse, QueryDict


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from currencyexchange.views import erase_all
from django.contrib.auth.models import User
from currencyexchange.models import Key, Access, Resource
from currencyexchange.tests.useful import add_user_and_key_to_bd, clear_tables, add_permission
from currencyexchange.tests.useful import add_courses_to_bd, add_feature_flag
from currencyexchange.tests.useful import IVAN_KEY


class AverageCourseTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        ivan = add_user_and_key_to_bd('IvanIvanov', 'Ivan', 'Ivanov', 'ivanMolodec', 'ivanov.ivan@mail.ru',
                               False, False, True, '07.08.2021')
        add_permission(id=ivan, access=Access.read, resource=Resource.rate)
        add_permission(id=ivan, access=Access.write, resource=Resource.rate)
        add_feature_flag(ivan[0])

        add_user_and_key_to_bd('AlexAlexandrov', 'Alex', 'Alexandrov', 'AlexXXX', 'Alex.Alexandrov@mail.ru',
                               False, False, True, '07.08.2021')


        #code, time, rate
        info=[('USD', "2021-03-05 13:25:13+00:00", 90),
              ('USD', "2021-03-05 13:20:13+00:00", 85),
              ('USD', "2021-03-05 13:19:13+00:00", 95),
              ('USD', "2021-03-06 13:25:13+00:00", 90),
              ('USD', "2021-03-06 13:20:13+00:00", 85),
              ('USD', "2021-03-06 13:19:13+00:00", 95),
              ('USD', "2021-03-07 13:25:13+00:00", 90),
              ('USD', "2021-03-07 13:20:13+00:00", 85),
              ('USD', "2021-03-07 13:19:13+00:00", 95),
              ('RUB', "2021-03-05 13:19:13+00:00", 1),
              ]
        add_courses_to_bd(info)

    @classmethod
    def tearDownClass(cls):
        clear_tables()

    def setUp(self) -> None:
        self.client = Client()

    def test_get_average_course_one_day(self):
        data = {
            "currency_code": "USD",
            "time": "2021-03-05",
        }
        response = self.client.post(path='/api/average_course', data=data, content_type='application/json',
                                    HTTP_API_USER_KEY=IVAN_KEY)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"Date": "2021-03-05", "Currency": "USD", "Average Course": 90.0}')

    def test_get_average_course_some_days(self):
        data = {
            "currency_code": "USD",
            "start_date": "2021-03-05",
            "end_date": "2021-03-07",
        }
        response = self.client.post(path='/api/average_course_some_days', data=data, content_type='application/json',
                                    HTTP_API_USER_KEY=IVAN_KEY)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, (b'[{"Date": "2021-03-05", "Currency": "USD", "Average Course": 90.0}, '
                                            b'{"Date": "2021-03-06", "Currency": "USD", "Average Course": 90.0}, '
                                            b'{"Date": "2021-03-07", "Currency": "USD", "Average Course": 90.0}]'))
