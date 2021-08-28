from rest_framework import serializers

from apps.sales.models import Sale


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = [
            'id',
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


class TotCashBackSerializer(serializers.Serializer):
    total_cashback = serializers.FloatField()
