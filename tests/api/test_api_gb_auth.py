from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.gb_auth.models import User


class ApiGbAuthTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='saiyajin',
            cpf='48527519003',
            email='test@test.com',
            first_name='Super',
            last_name='Saiyajin',
            password='123456'
        )

        url_get_token = reverse('api:token_obtain_pair')
        self.client = APIClient()
        resp = self.client.post(
            url_get_token,
            {
                'email': self.user.email,
                'password': '123456'
            },
            format='json'
        )
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_dealer_list(self):
        response = self.client.get('/api/dealer/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['results'][0]['id'],
            str(self.user.id)
        )

    def test_dealer_create(self):
        response = self.client.post(
            '/api/dealer/',
            data={
                'username': 'goku',
                'first_name': 'Goku',
                'last_name': 'Mil',
                'email': 'user@example.com',
                'cpf': '04953428404',
                'password': '123456'
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_dealer_update(self):
        response = self.client.put(
            f'/api/dealer/{self.user.id}/',
            data={
                'username': 'goku',
                'first_name': 'Super',
                'last_name': 'Mil',
                'email': 'user@example.com',
                'cpf': '04953428404',
                'password': '123456'
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_dealer_delete(self):
        response = self.client.delete(f'/api/dealer/{self.user.id}/')
        self.assertEqual(response.status_code, 204)
