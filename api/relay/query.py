import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from ..models import Movie, Director
from graphene_django.filter import DjangoFilterConnectionField


class MovieNode(DjangoObjectType):
    class Meta:
        model = Movie
        filter_fields = {
            "title": ["exact", "icontains", "istartswith"],
            "year": ["exact", "icontains", "istartswith"],
            "director": ["exact"],
        }
        interfaces = (relay.Node,)


class DirectorNode(DjangoObjectType):
    class Meta:
        model = Director
        filter_fields = {
            "name",
            "surname"
        }
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    all_movies = DjangoFilterConnectionField(MovieNode)
    movie = relay.Node.Field(MovieNode)
    all_directors = DjangoFilterConnectionField(DirectorNode)
