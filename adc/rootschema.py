from graphene.types import schema
from graphene_django import debug
import account.schema
import constants.schema
import transactions.schema
import expense.schema
import graphene
from graphene_django.debug import DjangoDebug


class Query(account.schema.Query, constants.schema.Query, expense.schema.Query,transactions.schema.Query,
                 graphene.ObjectType):
    debug=graphene.Field(DjangoDebug, name="_debug")

class Mutation(account.schema.Mutation, transactions.schema.Mutation, expense.schema.Mutation,graphene.ObjectType):
    debug=graphene.Field(DjangoDebug, name="_debug")



schema=graphene.Schema(query=Query, mutation=Mutation)