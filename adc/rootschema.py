from graphene.types import schema
from graphene_django import debug
import account.schema
import constants.schema
import transactions.schema
import expense.schema
import project.schema
import documents.schema
import graphene
from graphene_django.debug import DjangoDebug


class Query(account.schema.Query, constants.schema.Query, expense.schema.Query,transactions.schema.Query,
                 project.schema.Query , documents.schema.Query ,graphene.ObjectType):
    debug=graphene.Field(DjangoDebug, name="_debug")

class Mutation(account.schema.Mutation, transactions.schema.Mutation, expense.schema.Mutation,
                project.schema.Mutation, documents.schema.Mutation,graphene.ObjectType):
    debug=graphene.Field(DjangoDebug, name="_debug")



schema=graphene.Schema(query=Query, mutation=Mutation)