import graphene
import secrets
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from ...serializers.login import UserLoginSerializer, UserForgetPasswordSerializer, UserResetPasswordSerializer
from base.helper import send_passwordrest_email
from django.contrib.auth import authenticate
from graphql_jwt.shortcuts import get_token

User = get_user_model()


class UserLoginInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    password = graphene.String(required=True)


class UserLoginMutation(graphene.Mutation):
    class Arguments:
        input_data = UserLoginInput(required=True)

    message = graphene.String()
    status = graphene.Int()
    token = graphene.String()

    @staticmethod
    def mutate(root, info, input_data):
        try:
            serializer = UserLoginSerializer(data=input_data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']
                user = authenticate(request=info.context,
                                    email=email, password=password)

                if user is not None:
                    token = get_token(user)
                    return UserLoginMutation(
                        message='Login Successful',
                        status=200,
                        token=token
                    )
                else:
                    return UserLoginMutation(
                        message='Invalid email or password',
                        status=400,
                        token=None
                    )
            else:
                return UserLoginMutation(
                    message='Validation Error',
                    status=400,
                    token=None
                )
        except Exception as e:
            print(e)
            return UserLoginMutation(
                message='Internal Server Error',
                status=500,
                token=None
            )


class UserForgetPasswordInput(graphene.InputObjectType):
    email = graphene.String(required=True)


class UserForgetPasswordMutation(graphene.Mutation):
    class Arguments:
        input_data = UserForgetPasswordInput(required=True)

    message = graphene.String()
    status = graphene.Int()

    @staticmethod
    def mutate(root, info, input_data):
        try:
            serializer = UserForgetPasswordSerializer(data=input_data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                get_user = User.objects.filter(email=email)
                if get_user.exists():
                    user = get_user.first()
                    token = secrets.token_hex(16)
                    user.reset_token = token
                    user.save()
                    current_site = get_current_site(info.context)
                    reset_link = f"http://{current_site.domain}/password-reset/{token}"

                    send_passwordrest_email(email, reset_link)

                    # token_generator = PasswordResetTokenGenerator()
                    # uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                    # token = token_generator.make_token(user)
                    # current_site = get_current_site(info.context)
                    # relative_link = reverse('password_reset_confirm', kwargs={
                    #                         'uidb64': uidb64, 'token': token})
                    # reset_link = f"http://{current_site.domain}{relative_link}"

                    return UserForgetPasswordMutation(
                        message='Password reset link sent successfully',
                        status=200
                    )
                else:
                    return UserForgetPasswordMutation(
                        message='User not found',
                        status=404
                    )
            else:
                return UserForgetPasswordMutation(
                    message='Validation Error',
                    status=400
                )
        except Exception as e:
            print(e)
            return UserForgetPasswordMutation(
                message='Internal Server Error',
                status=500
            )

    def resolve_reset_link(root, info):
        return root.reset_link


class UserResetPasswordInput(graphene.InputObjectType):
    token = graphene.String(required=True)
    new_password = graphene.String(required=True)


class UserResetPasswordMutation(graphene.Mutation):
    class Arguments:
        input_data = UserResetPasswordInput(required=True)

    message = graphene.String()
    status = graphene.Int()

    @staticmethod
    def mutate(self, info, input_data):
        try:
            serializer = UserResetPasswordSerializer(data=input_data)
            if serializer.is_valid():
                token = serializer.validated_data['token']
                new_password = serializer.validated_data['new_password']

                user = User.objects.filter(reset_token=token).first()

                if user:
                    user.set_password(new_password)
                    user.reset_token = None
                    user.save()

                    return UserResetPasswordMutation(
                        message='Password reset successful',
                        status=200
                    )

                else:
                    return UserResetPasswordMutation(
                        message='Invalid token',
                        status=400
                    )

            else:
                return UserForgetPasswordMutation(
                    message='Validation Error',
                    status=400
                )

        except Exception as e:
            print(e)
            return UserResetPasswordMutation(
                message=str(e),
                status=500
            )
