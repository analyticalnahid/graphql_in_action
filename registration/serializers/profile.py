from rest_framework import serializers
from ..models import User


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    extra_kwargs = {'current_password': {'write_only': True},
                    'new_password': {'write_only': True}}


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class AccountDeletionSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    extra_kwargs = {'password': {'write_only': True}}


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'is_verified']
