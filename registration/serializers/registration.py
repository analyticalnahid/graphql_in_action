from rest_framework import serializers
from ..models import User
from base.helper.validation import validate_email, validate_password

from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, input_data):
        email = input_data['email']
        password = input_data['password']
        if email:
            validate_email(email)
        if password:
            validate_password(password)

        return input_data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'otp']
        extra_kwargs = {'otp': {'write_only': True}}

    def validate(self, input_data):
        email = input_data['email']
        if email:
            validate_email(email)

        return input_data
