from rest_framework import viewsets
from django_filters import rest_framework as filters

from apps.sales.models import Sale
from .serializers import SaleSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    filter_backends = (filters.DjangoFilterBackend,)
