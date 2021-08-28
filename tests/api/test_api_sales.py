from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.utils import timezone

from apps.gb_auth.models import User
from apps.sales.models import Sale


class ApiSalesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='saiyajin',
            cpf='48527519003',
            email='test@test.com',
            first_name='Super',
            last_name='Saiyajin',
            password='123456'
        )
        self.sale = Sale.objects.create(
            code='PE1234',
            value=123.12,
            date=timezone.now(),
            cpf=self.user
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

    def test_sale_create(self):
        response = self.client.post(
            '/api/sale/',
            data={
                'code': 'PE1234',
                'value': 1223.23,
                'date': '2021-08-28T15:13:15.380Z',
                'cpf': self.user
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_sale_list(self):
        response = self.client.get('/api/sale/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['results'][0]['code'],
            self.sale.code
        )

    def test_sale_update(self):
        response = self.client.put(
            f'/api/sale/{self.sale.id}/',
            data={
                'code': 'PE1234',
                'value': 1223.23,
                'date': '2021-08-27T15:13:15.380Z',
                'cpf': self.user
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_sale_delete(self):
        response = self.client.delete(f'/api/sale/{self.sale.id}/')
        self.assertEqual(response.status_code, 204)

    def test_sale_total_cashback(self):
        response = self.client.get(
            f'/api/sale/total_cashback/?cpf={self.user.cpf}'
        )
        self.assertEqual(response.status_code, 200)

    def test_sale_list_id(self):
        response = self.client.get(
            f'/api/sale/{self.sale.id}/'
        )
        self.assertEqual(response.status_code, 200)
