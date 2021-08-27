from django.test import TestCase
from django.core.exceptions import ValidationError

from apps.gb_auth.models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='saiyajin',
            cpf='48527519003',
            email='test@test.com',
            first_name='Super',
            last_name='Saiyajin',
            password='123456'
        )

    def test_create(self):
        user = User.objects.first()
        self.assertEqual(self.user, user)

    def test_validation_username(self):
        user = User(
            username='',
            cpf='16501398029',
            email='test1@test.com',
            first_name='Super',
            last_name='Saiyajin',
            password='123456'
        )
        self.assertRaises(ValidationError, user.full_clean)

    def test_validation_cpf(self):
        user = User(
            username='saiyajin',
            cpf='x',
            email='test1@test.com',
            first_name='Super',
            last_name='Saiyajin',
            password='123456'
        )
        self.assertRaises(ValidationError, user.full_clean)

    def test_validation_email(self):
        user = User(
            username='saiyajin',
            cpf='16501398029',
            email='test1',
            first_name='Super',
            last_name='Saiyajin',
            password='123456'
        )
        self.assertRaises(ValidationError, user.full_clean)
