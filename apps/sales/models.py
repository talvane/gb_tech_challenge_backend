import logging
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum
from django.core.exceptions import ValidationError

from apps.utils.mymodel import CommonModel

User = get_user_model()

logger = logging.getLogger(__name__)

CPF_APPROVED = '15350946056'
STATUS_APPROVED = 'AP'


def validate_value(value):
    if value <= 0:
        raise ValidationError(
            _('%(value)s value invalid.'),
            params={'value': value},
        )


class Sale(CommonModel):
    STATUS__CHOICES = (
        ('IN', _('In Validation')),
        ('AP', _('Approved')),
    )

    code = models.CharField(verbose_name=_('Product Code'), max_length=15)
    value = models.FloatField(
        verbose_name=_('Product Value'), validators=[validate_value]
    )
    date = models.DateTimeField(verbose_name=_('Date'))
    cpf = models.ForeignKey(
        User, to_field='cpf', db_column='cpf', verbose_name=_('Cpf'),
        on_delete=models.CASCADE
    )
    status = models.CharField(
        verbose_name=_('Status'), max_length=2,
        choices=STATUS__CHOICES, default='IN'
    )
    perc_cashback = models.FloatField(
        verbose_name=_('Percent Cashback apply'),
        validators=[MinValueValidator(0.01), MaxValueValidator(100)],
        editable=False, default=0
    )
    value_cashback = models.FloatField(
        verbose_name=_('Value Cashback apply'),
        editable=False, default=0
    )

    class Meta:
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')
        ordering = ('cpf',)

    def __str__(self):
        return f'{self.code} - {self.date.strftime("%m/%d/%Y, %H:%M:%S")}'

    def save(self, *args, **kwargs):
        self.calc_cashback()
        if self.cpf.cpf == CPF_APPROVED:
            self.status = STATUS_APPROVED
            logger.info(f'Sale approved for cpf {CPF_APPROVED}')
        return super(Sale, self).save(*args, **kwargs)

    @property
    def description_status(self):
        return self.get_status_display()

    def calc_cashback(self):
        cashback = CalcCashBack(
            cpf=self.cpf_id, date=self.date, value=self.value
        )
        dict_value = cashback.get_value()
        self.perc_cashback = dict_value['perc_cashback']
        self.value_cashback = dict_value['value_cashback']
        logger.info(
            f'Calc CashBack for id {self.id}, value {self.value_cashback}'
        )


class CalcCashBack():

    def __init__(self, cpf, date, value):
        self.cpf = cpf
        self.date = date
        self.value = value

    def get_value(self):
        tot_month_value = Sale.objects.filter(
            cpf_id=self.cpf, date__month=self.date.month
        ).aggregate(Sum('value'))

        if tot_month_value['value__sum']:
            val_index = tot_month_value['value__sum']
        else:
            val_index = self.value

        if val_index <= 1000:
            return {
                'perc_cashback': 10,
                'value_cashback': ((self.value * 10)/100)
            }
        elif val_index > 1000 and val_index <= 1500:
            return {
                'perc_cashback': 15,
                'value_cashback': ((self.value * 15)/100)
            }
        else:
            return {
                'perc_cashback': 20,
                'value_cashback': ((self.value * 20)/100)
            }
