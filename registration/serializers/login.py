from rest_framework import serializers
from ..models import User


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']


class UserResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()

    extra_kwargs = {'new_password': {'write_only': True},
                    'token': {'write_only': True}}
