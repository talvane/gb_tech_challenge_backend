from rest_framework import viewsets
from django_filters import rest_framework as filters

from apps.gb_auth.models import User
from .serializers import UserSerializer, UserSerializerPutPatch
from .filterset import UserFilter


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = UserFilter

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            serializer_class = UserSerializerPutPatch

        return serializer_class
