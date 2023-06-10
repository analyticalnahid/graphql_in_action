from django.core.validators import EmailValidator
from rest_framework import serializers


def validate_email(email):
    email_validator = EmailValidator()
    try:
        email_validator(email)
    except serializers.ValidationError as e:
        raise serializers.ValidationError({'email': e})


def validate_password(password):
    min_password_length = 8
    if len(password) < min_password_length:
        raise serializers.ValidationError(
            {'password': f'Password must be at least {min_password_length} characters long.'})


def get_error_details(serializer):
    error_messages = serializer.errors
    error_details = []
    for field, errors in error_messages.items():
        for error in errors:
            error_details.append({
                'field': field,
                'message': str(error),
                'code': error.code
            })
    return error_details
