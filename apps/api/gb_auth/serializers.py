import re
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

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

    def create(self, validated_data):
        validated_data['cpf'] = re.sub(r"[\W_]+", "", validated_data['cpf'])
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserSerializerPutPatch(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'password'
        ]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name
        )
        instance.last_name = validated_data.get(
            'last_name', instance.last_name
        )
        if validated_data.get('password', ''):
            instance.password = make_password(validated_data.get('password'))
        instance.save()

        return instance
