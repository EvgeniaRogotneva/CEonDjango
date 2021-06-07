import os, requests
import django, json
from django.test import TestCase, Client, RequestFactory
from django.http import HttpRequest, HttpResponse, QueryDict
from datetime import datetime, timedelta
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.auth.models import User
from currencyexchange.models import Key
import base64
auth_headers = {
    'HTTP_AUTHORIZATION': b'Basic ' + base64.b64encode(b'username:password'),
}


class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        #self.superuser = User(is_superuser=True, username='BigBoss', email='big@boss.com', password='GodBlessYou')
        #self.superuser.save()
        #self.key = Key(user=self.superuser, key='BigBossIsHere')
        #self.key.save()
        #data = {'username': 'IvanIvanov', 'email': 'ivanov.ivan@mail.ru', 'password': 'ivanMolodec',
        #        'key': 'IvanTsarevich'}
        #response = self.client.post(data=data, content_type='application/json', path='/api/create_user',
        #                            HTTP_API_USER_KEY='BigBossIsHere')
        #self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.content, b'{"Response": "User IvanIvanov has been added"}')

    def test_create_user_by_super(self):
        data = {'username': 'PetrPetrov', 'email': 'petrov.petr@mail.ru', 'password': 'PetrMolodec',
                'key': 'PetrPervij'}
        response = self.client.post(data=data, content_type='application/json', path='/api/create_user',
                                    HTTP_API_USER_KEY='BigBossIsHere')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{"Response": "User PetrPetrov has been added"}')

    def test_create_user(self):
        data = {'username': 'IvanIvanov', 'email': 'ivanov.ivan@mail.ru', 'password': 'ivanMolodec',
                'key': 'IvanTsarevich'}

        response = self.client.post(data=data, content_type='application/json', path='/api/create_user',
                                    HTTP_API_USER_KEY='smth_wrong')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'{"Error": "You do not have permission to add users"}')
