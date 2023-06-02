import graphene
from api.schema import Mutation as api_mutation
from api.schema import Query as api_query


class Query(api_query, graphene.ObjectType):
    pass

class Mutation(api_mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
