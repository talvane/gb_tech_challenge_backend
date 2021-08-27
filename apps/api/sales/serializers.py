from rest_framework import serializers

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
            'description_status',
            'perc_cashback',
            'value_cashback'
        ]
        ready_only_fields = ('status',)
