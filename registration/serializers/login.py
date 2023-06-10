from rest_framework import serializers
from ..models import User
from base.helper.validation import validate_email, validate_password


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, input_data):
        email = input_data['email']
        password = input_data['password']
        if email:
            validate_email(email)
        if password:
            validate_password(password)

        return input_data


class UserForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email']
        
    def validate(self, input_data):
        email = input_data['email']
        if email:
            validate_email(email)

        return input_data



class UserResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField()

    extra_kwargs = {'new_password': {'write_only': True},
                    'token': {'write_only': True}}
    
    def validate(self, input_data):
        new_password = input_data['new_password']
        if new_password:
            validate_password(new_password)

        return input_data
