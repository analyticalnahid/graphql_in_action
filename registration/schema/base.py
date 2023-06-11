import graphene
from .query import Query
from .mutation.base import Mutation

schema = graphene.Schema(query=Query,  mutation=Mutation)

# Remove Introspection type from the schema
schema.introspect = False
