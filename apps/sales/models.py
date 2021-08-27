import logging
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

from apps.utils.mymodel import CommonModel

User = get_user_model()

logger = logging.getLogger(__name__)

CPF_APPROVED = '15350946056'
STATUS_APPROVED = 'AP'


class Sale(CommonModel):
    STATUS__CHOICES = (
        ('IN', _('In Validation')),
        ('AP', _('Approved')),
    )

    code = models.CharField(verbose_name=_('Product Code'), max_length=15)
    value = models.FloatField(verbose_name=_('Product Value'))
    date = models.DateTimeField(verbose_name=_('Date'))
    cpf = models.ForeignKey(
        User, to_field='cpf', db_column='cpf', verbose_name=_('Cpf'),
        on_delete=models.CASCADE
    )
    status = models.CharField(
        verbose_name=_('Status'), max_length=2,
        choices=STATUS__CHOICES, default='IN'
    )

    class Meta:
        verbose_name = _('Sale')
        verbose_name_plural = _('Sales')
        ordering = ('cpf',)

    def __str__(self):
        return f'{self.code} - {self.date.strftime("%m/%d/%Y, %H:%M:%S")}'

    def save(self, *args, **kwargs):
        if self.cpf.cpf == CPF_APPROVED:
            self.status = STATUS_APPROVED
        return super(Sale, self).save(*args, **kwargs)
