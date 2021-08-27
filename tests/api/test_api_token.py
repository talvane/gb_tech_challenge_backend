from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from apps.gb_auth.models import User


class ApiTokenTest(TestCase):
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
        self.token = resp.data['access']
        self.token_refresh = resp.data['refresh']

    def test_token_refresh(self):
        url_get_token = reverse('api:token_refresh')
        resp = self.client.post(
            url_get_token,
            {
                'refresh': self.token_refresh
            },
            format='json'
        )
        self.assertEqual(resp.status_code, 200)

    def test_token_verify(self):
        url_get_token = reverse('api:token_verify')
        resp = self.client.post(
            url_get_token,
            {
                'token': self.token
            },
            format='json'
        )
        self.assertEqual(resp.status_code, 200)
