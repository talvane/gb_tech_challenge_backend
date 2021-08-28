from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.gb_auth.models import User
from apps.sales.models import Sale, CalcCashBack


class SaleModelTest(TestCase):
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

    def test_create(self):
        sale = Sale.objects.first()
        self.assertEqual(self.sale, sale)

    def test_validation_code(self):
        sale = Sale(
            code='',
            value=123.12,
            date=timezone.now(),
            cpf=self.user
        )
        self.assertRaises(ValidationError, sale.full_clean)

    def test_validation_value(self):
        sale = Sale(
            code='PE1234',
            value=0,
            date=timezone.now(),
            cpf=self.user
        )
        self.assertRaises(ValidationError, sale.full_clean)

    def test_validation_date(self):
        sale = Sale(
            code='PE1234',
            value=654.23,
            cpf=self.user
        )
        self.assertRaises(ValidationError, sale.full_clean)

    def test_validation_cpf(self):
        sale = Sale(
            code='PE1234',
            value=654.23,
            date=timezone.now()
        )
        self.assertRaises(ValidationError, sale.full_clean)


class CalcCashBackTest(TestCase):
    def setUp(self):
        self.cpf = '48527519003'
        self.date = timezone.now()
        self.value_10_perc = 123.12
        self.value_15_perc = 1124.34
        self.value_20_perc = 1754.11

    def test_10_perc(self):
        perc_cashback_expect = 10
        value_cashback_expect = ((self.value_10_perc * 10)/100)
        cashback = CalcCashBack(
            cpf=self.cpf, date=self.date, value=self.value_10_perc
        )
        dict_value = cashback.get_value()
        self.assertEqual(perc_cashback_expect, dict_value['perc_cashback'])
        self.assertEqual(value_cashback_expect, dict_value['value_cashback'])

    def test_15_perc(self):
        perc_cashback_expect = 15
        value_cashback_expect = ((self.value_15_perc * 15)/100)
        cashback = CalcCashBack(
            cpf=self.cpf, date=self.date, value=self.value_15_perc
        )
        dict_value = cashback.get_value()
        self.assertEqual(perc_cashback_expect, dict_value['perc_cashback'])
        self.assertEqual(value_cashback_expect, dict_value['value_cashback'])

    def test_20_perc(self):
        perc_cashback_expect = 20
        value_cashback_expect = ((self.value_20_perc * 20)/100)
        cashback = CalcCashBack(
            cpf=self.cpf, date=self.date, value=self.value_20_perc
        )
        dict_value = cashback.get_value()
        self.assertEqual(perc_cashback_expect, dict_value['perc_cashback'])
        self.assertEqual(value_cashback_expect, dict_value['value_cashback'])
