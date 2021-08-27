from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.sales.models import Sale
from .serializers import SaleSerializer, TotCashBackSerializer
from .filterset import SaleFilter
from backend.services import TotCashBack


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SaleFilter

    @action(
        detail=True,
        methods=['get'],
        serializer_class=TotCashBackSerializer,
    )
    def total_cashback(self, request, **kwargs):
        tot_cashback = TotCashBack()
        tot_cashback.get_total(kwargs['pk'])

        if not tot_cashback.status_code == 200:
            return Response({}, tot_cashback.status_code)

        serializer = self.get_serializer(tot_cashback)
        return Response(serializer.data, status.HTTP_200_OK)
