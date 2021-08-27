from rest_framework import serializers

from apps.sales.models import Sale


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        exclude = [
            'id',
            'created_at',
            'updated_at'
        ]
        ready_only_fields = ('status',)
