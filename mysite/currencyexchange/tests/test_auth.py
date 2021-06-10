import os, requests
import django, json, psycopg2
from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest, HttpResponse, QueryDict
from datetime import datetime, timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
# from django.contrib.auth.models import User
# from currencyexchange.models import Key
from psycopg2 import OperationalError
import base64


def add_key_to_bd(username, id):
    conn = psycopg2.connect(host='127.0.0.1', database='currencyexchange', user='postgres', password='root')
    conn.autocommit = True
    s = "insert into currencyexchange_key (user_id, key) values ('{}', '{}');".format(
        id, base64.b64encode(username.encode()).decode('ascii'))
    cur = conn.cursor()
    print(cur.execute(s))
    print(conn)


def add_user_and_key_to_bd(username, first_name, last_name, password, email, is_superuser=False, is_staff=False,
                           is_active=True, date_joined=datetime.date):
    conn = psycopg2.connect(host='127.0.0.1', database='currencyexchange', user='postgres', password='root')
    conn.autocommit = True
    s = "insert into auth_user (username, first_name, last_name, password, email, is_superuser, is_staff, " \
        "is_active, date_joined) values ('{}', '{}', '{}', '{}', '{}', {}, {}, {}, '{}') returning id;"\
        .format(username, first_name, last_name, password, email, is_superuser, is_staff, is_active, date_joined)
    cur = conn.cursor()
    cur.execute(s)
    id = cur.fetchone()
    add_key_to_bd(username, id[0])


def remove_keys_and_users():
    conn = psycopg2.connect(host='127.0.0.1', database='currencyexchange', user='postgres', password='root')
    conn.autocommit = True
    s = 'delete from currencyexchange_key *'
    cur = conn.cursor()
    cur.execute(s)
    s = 'delete from auth_user *'
    cur = conn.cursor()
    cur.execute(s)


class AuthTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        remove_keys_and_users()

    def setUp(self):
        self.client = Client()

    @classmethod
    def setUpTestData(cls):
        add_user_and_key_to_bd('BigBoss', 'Big', 'Boss', 'GodBlessYou', 'big@boss.com',
                               True, True, True, '07.08.2021')
        add_user_and_key_to_bd('JohnSmith', 'John', 'Smith', 'JohnJohnJohn', 'john.smith@mail.ru',
                               False, False, True, '07.08.2021')

    def test_create_user_by_super(self):
        data = {'username': 'PetrPetrov', 'email': 'petrov.petr@mail.ru', 'password': 'PetrMolodec',
                'key': 'PetrPervij'}
        response = self.client.post(data=data, content_type='application/json', path='/api/create_user',
                                    HTTP_API_USER_KEY='QmlnQm9zcw==')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"Response": "User PetrPetrov has been added"}')

    def test_create_user(self):
        data = {'username': 'IvanIvanov', 'email': 'ivanov.ivan@mail.ru', 'password': 'ivanMolodec',
                'key': 'IvanTsarevich'}

        response = self.client.post(data=data, content_type='application/json', path='/api/create_user',
                                    HTTP_API_USER_KEY='smth_wrong')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.content, b'{"Error": "You are not authentificated"}')
