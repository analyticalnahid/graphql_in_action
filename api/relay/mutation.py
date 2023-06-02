import graphene
from ..models import Movie
from graphene import relay
from .query import MovieNode
import graphql_jwt
from graphql_relay import from_global_id


class MovieCreate(relay.ClientIDMutation):
    class Input:
        title = graphene.String(required=True)
        year = graphene.Int(required=True)

    movie = graphene.Field(MovieNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        movie = Movie(title=input.get('title'), year=input.get('year'))
        movie.save()

        return MovieCreate(movie=movie)


class MovieUpdate(relay.ClientIDMutation):
    class Input:
        movie_id = graphene.ID(required=True)
        title = graphene.String()
        year = graphene.Int()

    movie = graphene.Field(MovieNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        movie_id = from_global_id(input.get('movie_id'))[1]
        title = input.get('title')
        year = input.get('year')

        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            raise Exception("Movie not found")

        if title is not None:
            movie.title = title
        if year is not None:
            movie.year = year

        movie.save()

        return MovieUpdate(movie=movie)


class MovieDelete(relay.ClientIDMutation):
    class Input:
        movie_id = graphene.ID(required=True)

    movie_id = graphene.ID()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        movie_id = input.get('movie_id')

        try:
            movie = Movie.objects.get(pk=movie_id)
            movie.delete()
        except Movie.DoesNotExist:
            raise Exception("Movie not found")

        return MovieDelete(movie_id=movie_id)


class Mutation(graphene.ObjectType):

    token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.relay.Verify.Field()
    refresh_token = graphql_jwt.relay.Refresh.Field()
    delete_token_cookie = graphql_jwt.relay.DeleteJSONWebTokenCookie.Field()
    revoke_token = graphql_jwt.relay.Revoke.Field()
    
    create_movie = MovieCreate.Field()
    update_movie = MovieUpdate.Field()
    delete_movie = MovieDelete.Field()
