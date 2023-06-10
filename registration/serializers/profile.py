from rest_framework import serializers
from ..models import User
from base.helper.validation import validate_password


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    extra_kwargs = {'current_password': {'write_only': True},
                    'new_password': {'write_only': True}}

    def validate(self, input_data):
        current_password = input_data['current_password']
        new_password = input_data['new_password']

        if new_password and current_password:
            validate_password(new_password)

        if new_password == current_password:
            raise serializers.ValidationError(
                'New password and current password are same')

        return input_data


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class AccountDeletionSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    extra_kwargs = {'password': {'write_only': True}}

    def validate(self, input_data):
        password = input_data['password']

        if password:
            validate_password(password)

        return input_data


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'is_verified']
