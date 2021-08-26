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
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username')
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.email = validated_data.get('email')
        instance.cpf = validated_data.get('cpf')
        instance.password = make_password(validated_data.get('password'))
        instance.save()
        return instance
