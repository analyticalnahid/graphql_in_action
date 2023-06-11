import graphene
from graphene_django import DjangoObjectType
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from graphql import GraphQLError

User = get_user_model()


class UserType(DjangoObjectType):
    """
    Type definition for a single user.

    This object type represents a user in the system.
    """
    class Meta:
        model = User
        description = "Type definition for a single user"
        fields = ('id', 'email', 'first_name', 'last_name', 'is_verified')

    id = graphene.Int(description="The ID of the user")
    email = graphene.String(description="The email address of the user")
    first_name = graphene.String(description="The first name of the user")
    last_name = graphene.String(description="The last name of the user")
    is_verified = graphene.Boolean(
        description="Flag indicating if the user is verified")


class Query(graphene.ObjectType):
    all_users = graphene.List(
        UserType, description="Returns a list of all users")
    user = graphene.Field(UserType, id=graphene.Int(
        description="The ID of the user"), description="Return a single user by id")

    def resolve_all_users(self, info, **kwargs):
        if not info.context.user.is_authenticated:  # Check if the user is authenticated
            raise GraphQLError('Authentication required')
        return User.objects.all()

    def resolve_user(self, info, id):
        if not info.context.user.is_authenticated:  # Check if the user is authenticated
            raise GraphQLError('Authentication required')
        return get_object_or_404(User, pk=id)
