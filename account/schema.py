import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required
import graphql_jwt

class UserType(DjangoObjectType):
    class Meta:
        model=User
        fields=('username','first_name','last_name')

class Query(graphene.ObjectType):
    me=graphene.Field(UserType)

    @login_required
    def resolve_me(self, info):
        return info.context.user

class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
