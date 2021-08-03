import os
import django
from django.test import TestCase, Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from currencyexchange.models import Access, Resource
from currencyexchange.tests.useful import add_user_and_key_to_bd, clear_tables, add_permission
from currencyexchange.tests.useful import SUPER_KEY


class AuthTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        tables = []
        clear_tables()

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
                                    HTTP_API_USER_KEY=SUPER_KEY)
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
        response = self.client.get('/api/erase_all', HTTP_API_USER_KEY=SUPER_KEY)
        self.assertEqual(response.status_code, 200)
