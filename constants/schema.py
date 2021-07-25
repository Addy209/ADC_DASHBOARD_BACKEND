import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from graphql_jwt.decorators import login_required
import graphql_jwt
from .models import *

class MonthType(DjangoObjectType):
    class Meta:
        model=Month
        fields=['code','month']

class YearType(DjangoObjectType):
    class Meta:
        model=Year
        fields=['year']

class ModuleType(DjangoObjectType):
    class Meta:
        model=Module
        fields=['code','module']

class Query(graphene.ObjectType):
    month=graphene.List(MonthType)
    year=graphene.List(YearType)
    module=graphene.List(ModuleType)

    def resolve_month(self, info):
        return Month.objects.all()

    def resolve_year(self, info):
        return Year.objects.all()

    def resolve_module(self, info):
        return Module.objects.all()

