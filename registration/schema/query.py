import graphene
from graphene_django import DjangoObjectType
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from graphql import GraphQLError

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'email','first_name', 'last_name', 'is_verified')


class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int())

    def resolve_all_users(self, info, **kwargs):
        if not info.context.user.is_authenticated:  # Check if the user is authenticated
            raise GraphQLError('Authentication required')
        return User.objects.all()

    def resolve_user(self, info, id):
        if not info.context.user.is_authenticated:  # Check if the user is authenticated
            raise GraphQLError('Authentication required')
        return get_object_or_404(User, pk=id)