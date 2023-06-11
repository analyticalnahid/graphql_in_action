import graphene
from django.contrib.auth import get_user_model
from graphql import GraphQLError
from ...serializers.profile import ChangePasswordSerializer, AccountUpdateSerializer, AccountDeletionSerializer
from base.helper.validation import get_error_details

User = get_user_model()


class ChangePasswordInput(graphene.InputObjectType):
    current_password = graphene.String(
        required=True, description="The current password of the user")
    new_password = graphene.String(
        required=True, description="The new password of the user")


class ChangePasswordMutation(graphene.Mutation):
    class Arguments:
        input_data = ChangePasswordInput(
            required=True, description="Input data for changing password")

    message = graphene.String(description="Message for the user")
    status = graphene.Int(description="Status code for the response")

    @staticmethod
    def mutate(self, info, input_data):
        try:
            serializer = ChangePasswordSerializer(
                data=input_data, context={'request': info.context})
            if serializer.is_valid():
                user = info.context.user
                current_password = serializer.validated_data['current_password']
                new_password = serializer.validated_data['new_password']

                if not user.check_password(current_password):
                    raise GraphQLError('Invalid password.')

                user.set_password(new_password)
                user.save()

                return ChangePasswordMutation(
                    message='Password changed successfully.',
                    status=200
                )
            else:
                error_details = get_error_details(serializer)
                return ChangePasswordMutation(
                    message=error_details[0]['message'],
                    status=500,
                )
        except Exception as e:
            print(e)
            return ChangePasswordMutation(
                message=str(e),
                status=500
            )


class AccountUpdateInput(graphene.InputObjectType):
    first_name = graphene.String(
        required=False, description="The first name of the user")
    last_name = graphene.String(
        required=False, description="The last name of the user")


class AccountUpdateMutation(graphene.Mutation):
    class Arguments:
        input_data = AccountUpdateInput(
            required=False, description="Input data for updating account")

    message = graphene.String(description="Message for the user")
    status = graphene.Int(description="Status code for the response")

    @staticmethod
    def mutate(self, info, input_data):

        try:
            user = info.context.user
            for key, value in input_data.items():
                setattr(user, key, value)

            user.save()
            return AccountUpdateMutation(message='Account updated successfully.', status=200)
        except Exception as e:
            print(e)
            return AccountUpdateMutation(
                message=str(e),
                status=500
            )


class AccountDeletionInput(graphene.InputObjectType):
    password = graphene.String(
        required=True, description="The password of the user")


class AccountDeletionMutation(graphene.Mutation):
    class Arguments:
        input_data = AccountDeletionInput(
            required=True, description="Input data for deleting account")

    message = graphene.String(description="Message for the user")
    status = graphene.Int(description="Status code for the response")

    @staticmethod
    def mutate(self, info, input_data):
        try:
            serializer = AccountDeletionSerializer(
                data=input_data, context={'request': info.context})
            if serializer.is_valid():
                user = info.context.user
                password = serializer.validated_data['password']

                if not user.check_password(password):
                    raise GraphQLError('Invalid password.')

                user.delete()
                return AccountDeletionMutation(message='Account deleted successfully.', status=200)
            else:
                error_details = get_error_details(serializer)
                return AccountDeletionMutation(
                    message=error_details[0]['message'],
                    status=500,
                )
        except Exception as e:
            print(e)
            return AccountDeletionMutation(
                message=str(e),
                status=500
            )
