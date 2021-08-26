from rest_framework import viewsets
from django_filters import rest_framework as filters

from apps.gb_auth.models import User
from .serializers import UserSerializer
from .filterset import UserFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = UserFilter
