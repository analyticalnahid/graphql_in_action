import graphene
from graphene_django import DjangoObjectType
from ..models import Movie, Director
from graphql_jwt.decorators import login_required


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie
        fields = ("id", "title", "year", "director")

    movie_age = graphene.String()

    def resolve_movie_age(self, info):
        return "Old Movie" if self.year < 2000 else "New Movie"


class DirectorType(DjangoObjectType):
    class Meta:
        model = Director
        fields = ("name", "surname")


class Query(graphene.ObjectType):
    all_movies = graphene.List(MovieType)
    movie = graphene.Field(MovieType, id=graphene.Int(),
                           title=graphene.String())

    @login_required
    def resolve_all_movies(self, info, **kwargs):
        return Movie.objects.all()
        # user = info.context.user
        # if user.is_authenticated:
        #     return Movie.objects.all()
        # else:
        #     print("Authentication Error")

    def resolve_movie(self, info, **kwargs):
        id = kwargs.get("id")
        title = kwargs.get("title")

        if id is not None:
            return Movie.objects.get(pk=id)

        if title is not None:
            return Movie.objects.get(title=title)

        return None

    all_directors = graphene.List(DirectorType)

    def resolve_all_directors(self, info):
        return Director.objects.all()
