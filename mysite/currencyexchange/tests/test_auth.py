import os
import django, json, psycopg2
from django.test import TestCase, Client
from datetime import datetime
import base64
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from currencyexchange.models import Access, Resource


def add_key_to_bd(username, id):
    conn = psycopg2.connect(host='127.0.0.1', database='currencyexchange', user='postgres', password='root')
    conn.autocommit = True
    print('json permission', json.dumps({'add_rate': True, 'remove_rate': False, 'get_rate': True}))
    s = "insert into currencyexchange_key (user_id, key) values ('{}', '{}');".format(
        id, base64.b64encode(username.encode()).decode('ascii'))
    print('s', s)
    cur = conn.cursor()
    cur.execute(s)


def add_user_and_key_to_bd(username, first_name, last_name, password, email, is_superuser=False, is_staff=False,
                           is_active=True, date_joined=datetime.date):
    conn = psycopg2.connect(host='127.0.0.1', database='currencyexchange', user='postgres', password='root')
    conn.autocommit = True
    s = "insert into auth_user (username, first_name, last_name, password, email, is_superuser, is_staff, " \
        "is_active, date_joined) values ('{}', '{}', '{}', '{}', '{}', {}, {}, {}, '{}') returning id;" \
        .format(username, first_name, last_name, password, email, is_superuser, is_staff, is_active, date_joined)
    cur = conn.cursor()
    cur.execute(s)
    id = cur.fetchone()
    add_key_to_bd(username, id[0])
    return id


def remove_keys_and_users():
    conn = psycopg2.connect(host='127.0.0.1', database='currencyexchange', user='postgres', password='root')
    conn.autocommit = True
    s = 'delete from currencyexchange_key *'
    cur = conn.cursor()
    cur.execute(s)
    s = 'delete from currencyexchange_permission *'
    cur = conn.cursor()
    cur.execute(s)
    s = 'delete from auth_user *'
    cur = conn.cursor()
    cur.execute(s)


def add_permission(id, access, resource):
    conn = psycopg2.connect(host='127.0.0.1', database='currencyexchange', user='postgres', password='root')
    conn.autocommit = True
    s = "insert into currencyexchange_permission (access, resource, user_id) values ('{}', '{}', '{}');" \
        .format(access, resource, id[0])
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
        superuser = add_user_and_key_to_bd('BigBoss', 'Big', 'Boss', 'GodBlessYou', 'big@boss.com',
                                           True, True, True, '07.08.2021')
        for access in Access:
            for resource in Resource:
                add_permission(id=superuser, access=access, resource=resource)
        jhon = add_user_and_key_to_bd('JohnSmith', 'John', 'Smith', 'JohnJohnJohn', 'john.smith@mail.ru',
                                      False, False, True, '07.08.2021')
        add_permission(id=jhon, access=Access.read, resource=Resource.rate)

    def test_create_user_by_super(self):
        data = {'username': 'PetrPetrov', 'email': 'petrov.petr@mail.ru', 'password': 'PetrMolodec',
                'key': 'PetrPervij', 'permissions': {'add_rate': True, 'remove_rate': False, 'get_rate': True}}
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

    def test_erase_all(self):
        response = self.client.get('/api/erase_all', HTTP_API_USER_KEY="QmlnQm9zcw==")
        print('response', response)
        self.assertEqual(response.status_code, 200)
