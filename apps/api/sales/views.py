from rest_framework import viewsets, status
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.translation import ugettext as _

from apps.sales.models import Sale
from .serializers import SaleSerializer, TotCashBackSerializer
from .filterset import SaleFilter, TotCashBackFilter
from backend.services import TotCashBack


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SaleFilter

    @action(
        detail=False,
        methods=['get'],
        serializer_class=TotCashBackSerializer,
        filter_class=TotCashBackFilter,
        pagination_class=None
    )
    def total_cashback(self, request, **kwargs):
        if not request.query_params.get('cpf'):
            return Response(
                {
                    'detail': _('Cpf not informed.')
                },
                status.HTTP_400_BAD_REQUEST
            )

        tot_cashback = TotCashBack()
        tot_cashback.get_total(request.query_params['cpf'])

        if not tot_cashback.status_code == 200:
            return Response({}, tot_cashback.status_code)

        serializer = self.get_serializer(tot_cashback)
        return Response(serializer.data, status.HTTP_200_OK)
