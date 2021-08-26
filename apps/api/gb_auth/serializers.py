import re
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext as _

from apps.gb_auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'cpf',
            'password'
        ]

    def validate_username(self, value):
        if User.objects.filter(username=value.lower()).exists():
            raise serializers.ValidationError(_('Username already exists.'))
        return value

    def validate_first_name(self, value):
        return value.capitalize()

    def validate_last_name(self, value):
        return value.capitalize()

    def validate_cpf(self, value):
        normalize_cpf = re.sub(r"[\W_]+", "", value)
        if User.objects.filter(cpf=normalize_cpf).exists():
            raise serializers.ValidationError(_('CPF already exists.'))
        return normalize_cpf

    def validate_password(self, value):
        password = make_password(value)
        return password
