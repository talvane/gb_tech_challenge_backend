from django_filters.filters import ChoiceFilter, DateFromToRangeFilter
from django.utils.translation import ugettext as _
from django_filters import FilterSet, CharFilter

from apps.utils.filterset import SearchFilterSet
from apps.sales.models import Sale


FILTER_CHOICES = [
    ('IN', _('In Validation')),
    ('AP', _('Approved')),
]


class SaleFilter(SearchFilterSet):
    date = DateFromToRangeFilter()
    filter_by = ChoiceFilter(choices=FILTER_CHOICES, method='filter_by_value')

    class Meta:
        model = Sale
        fields = ['q', 'date', 'filter_by']
        search_fields = [
            'code__icontains',
            'cpf__cpf__icontains'
        ]

    def filter_by_value(self, queryset, name, value):
        if(value == 'IN'):
            return queryset.filter(status='IN')
        elif(value == 'AP'):
            return queryset.filter(status='AP')
        return queryset


class TotCashBackFilter(FilterSet):
    cpf = CharFilter(required=True)

    class Meta:
        model = Sale
        fields = ['cpf']
