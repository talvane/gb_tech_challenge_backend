from rest_framework import serializers
from django.utils.translation import gettext as _

from apps.sales.models import Sale


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = [
            'code',
            'value',
            'date',
            'cpf',
            'status',
            'description_status'
        ]
        ready_only_fields = ('status',)

    def validate_value(self, value):
        if value <= 0:
            raise serializers.ValidationError(_('Value invalid.'))
        return value
