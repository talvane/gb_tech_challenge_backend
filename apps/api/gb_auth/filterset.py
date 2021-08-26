from apps.utils.filterset import SearchFilterSet
from apps.gb_auth.models import User


class UserFilter(SearchFilterSet):
    class Meta:
        model = User
        fields = ['q']
        search_fields = [
            'username__icontains',
            'first_name__icontains',
            'last_name__icontains',
            'cpf__icontains'
        ]
