import graphene
from django.contrib.auth import get_user_model
from ..query import UserType
from ...serializers.registration import UserRegistrationSerializer, VerifyAccountSerializer
from base.helper.mail_otp import send_otp_via_email, generate_otp
from base.helper.validation import get_error_details

User = get_user_model()


class UserRegistrationInput(graphene.InputObjectType):
    email = graphene.String(
        required=True, description="The email address of the user")
    password = graphene.String(
        required=True, description="The password of the user")


class UserRegistrationMutation(graphene.Mutation):
    class Arguments:
        input_data = UserRegistrationInput(
            required=True, description="Input data for user registration")

    message = graphene.String(description="Message for the user")
    status = graphene.Int(description="Status code for the response")
    user = graphene.Field(
        lambda: UserType, description="User object for the registered user")

    @staticmethod
    def mutate(root, info, input_data):
        try:
            email = input_data.email

            existing_user = User.objects.filter(email=email).first()
            if existing_user:
                return UserRegistrationMutation(
                    message='User already exists',
                    status=400,
                    user=None,
                )

            serializer = UserRegistrationSerializer(data=input_data)
            if serializer.is_valid():
                user = serializer.save()
                email = serializer.validated_data['email']
                otp = generate_otp()
                send_otp_via_email(email, otp)
                return UserRegistrationMutation(
                    message='Registration Successful. Check your email for OTP.',
                    status=200,
                    user=user,
                )
            else:
                error_details = get_error_details(serializer)
                return UserRegistrationMutation(
                    message=error_details[0]['message'],
                    status=500,
                    user=None,
                )

        except Exception as e:
            print(e)
            return UserRegistrationMutation(
                message='Internal Server Error',
                status=500,
                user=None,
            )


class VerifyAccountInput(graphene.InputObjectType):
    email = graphene.String(required=True, description="The email address of the user")
    otp = graphene.String(required=True, description="The OTP sent to the user")


class VerifyOTPMutation(graphene.Mutation):
    class Arguments:
        input_data = VerifyAccountInput(required=True, description="Input data for OTP verification")

    message = graphene.String(description="Message for the user")
    status = graphene.Int(description="Status code for the response")

    @staticmethod
    def mutate(root, info, input_data):
        try:
            serializer = VerifyAccountSerializer(data=input_data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                otp = serializer.validated_data['otp']
                User = get_user_model()
                user = User.objects.filter(email=email).first()

                if user:
                    if user.is_verified:
                        return VerifyOTPMutation(
                            message='User already verified',
                            status=400,
                        )
                    elif user.otp == otp:
                        user.is_verified = True
                        user.otp = None
                        user.save()
                        return VerifyOTPMutation(
                            message='OTP Verified',
                            status=200,
                        )
                    else:
                        return VerifyOTPMutation(
                            message='Wrong OTP',
                            status=400,
                        )
                else:
                    return VerifyOTPMutation(
                        message='User not found',
                        status=404,
                    )
            else:
                error_details = get_error_details(serializer)
                return VerifyOTPMutation(
                    message=error_details[0]['message'],
                    status=500,
                )
        except Exception as e:
            print(e)
            return VerifyOTPMutation(
                message='Internal Server Error',
                status=500,
            )
