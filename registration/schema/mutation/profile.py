import graphene
from django.contrib.auth import get_user_model
from graphql import GraphQLError
from ...serializers.profile import ChangePasswordSerializer, AccountUpdateSerializer, AccountDeletionSerializer


User = get_user_model()



class ChangePasswordInput(graphene.InputObjectType):
    current_password = graphene.String(required=True)
    new_password = graphene.String(required=True)


class ChangePasswordMutation(graphene.Mutation):
    class Arguments:
        input_data = ChangePasswordInput(required=True)

    message = graphene.String()
    status = graphene.Int()

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
                return ChangePasswordMutation(
                    message='Validation Error',
                    status=400
                )

        except Exception as e:
            print(e)
            return ChangePasswordMutation(
                message=str(e),
                status=500
            )


class AccountUpdateInput(graphene.InputObjectType):
    first_name = graphene.String(required=False)
    last_name = graphene.String(required=False)


class AccountUpdateMutation(graphene.Mutation):
    class Arguments:
        input_data = AccountUpdateInput(required=False)

    message = graphene.String()
    status = graphene.Int()

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
    password = graphene.String(required=True)


class AccountDeletionMutation(graphene.Mutation):
    class Arguments:
        input_data = AccountDeletionInput(required=True)

    message = graphene.String()
    status = graphene.Int()

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
                return AccountDeletionMutation(message='Validation Error',
                                               status=400)
        except Exception as e:
            print(e)
            return AccountDeletionMutation(
                message=str(e),
                status=500
            )


