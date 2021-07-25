import graphene
from graphene_django import DjangoObjectType
from .models import *
from graphql_jwt.decorators import login_required
import graphql_jwt
from graphene_file_upload.scalars import Upload

class TransactionType(DjangoObjectType):
    class Meta:
        model=DailyTransaction
        fields='__all__'

# ("date","mb_fintxns","mb_nonfintxns","mb_totaltxn","mb_td","mb_td_percent","mb_bd",
#                 "upi_fintxns","upi_nonfintxns","upi_totaltxn","upi_td","upi_td_percent","upi_bd",
#                 "imps_totaltxn","imps_td","imps_td_percent","imps_bd")

class Query(graphene.ObjectType):
    transaction=graphene.List(TransactionType, fromdate=graphene.Date(required=False), todate=graphene.Date(required=False))
    fifteendaytd=graphene.List(TransactionType)
    todaydata=graphene.Field(TransactionType)

    @login_required
    def resolve_transaction(self, info, fromdate, todate):
        if fromdate and todate:
            return DailyTransaction.getDatabetweenspecifieddates(fromdate,todate)
        else:
            return DailyTransaction.fifteendaydata()

    @login_required
    def resolve_fifteendaytd(self,info):
              
        td=DailyTransaction()
        return td.fifteendaydata()
    
    @login_required
    def resolve_todaydata(self, info):
        return DailyTransaction.todaydata()


class UpdateFromFile(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    def mutate(self, info, file, **kwargs):
        print(file)
        DailyTransaction.createEntry(file)

        return UpdateFromFile(success=True)

class Mutation(graphene.ObjectType):
    upload=UpdateFromFile.Field()