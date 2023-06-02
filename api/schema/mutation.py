import graphene
from ..models import Movie
from .query import MovieType
import graphql_jwt


class MovieCreate(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        year = graphene.Int(required=True)

    movie = graphene.Field(MovieType)

    def mutate(self, info, title, year):
        movie = Movie.objects.create(title=title, year=year)

        return MovieCreate(movie=movie)


class MovieUpdate(graphene.Mutation):
    class Arguments:
        movie_id = graphene.ID(required=True)
        title = graphene.String()
        year = graphene.Int()

    movie = graphene.Field(MovieType)

    def mutate(self, info, movie_id, title=None, year=None):
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


class MovieDelete(graphene.Mutation):
    class Arguments:
        movie_id = graphene.ID(required=True)

    movie_id = graphene.ID()

    def mutate(self, info, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
            movie.delete()
        except Movie.DoesNotExist:
            raise Exception("Movie not found")

        return MovieDelete(f"This {movie_id} of Movie Deleted Successfully")


class Mutation(graphene.ObjectType):

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()

    verify_token = graphql_jwt.Verify.Field()

    delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()

    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()

    create_movie = MovieCreate.Field()
    update_movie = MovieUpdate.Field()
    delete_movie = MovieDelete.Field()
