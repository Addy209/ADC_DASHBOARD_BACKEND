from django.db.models import fields
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

class TotalUserType(DjangoObjectType):
    class Meta:
        model=TotalUsers
        fields="__all__"


class IncUserType(DjangoObjectType):
    class Meta:
        model=IncrementalUser
        fields="__all__"
        

# ("date","mb_fintxns","mb_nonfintxns","mb_totaltxn","mb_td","mb_td_percent","mb_bd",
#                 "upi_fintxns","upi_nonfintxns","upi_totaltxn","upi_td","upi_td_percent","upi_bd",
#                 "imps_totaltxn","imps_td","imps_td_percent","imps_bd")

class Query(graphene.ObjectType):
    transaction=graphene.List(TransactionType, fromdate=graphene.Date(required=False), todate=graphene.Date(required=False))
    fifteendaytd=graphene.List(TransactionType)
    todaydata=graphene.Field(TransactionType)
    incuserdata=graphene.List(IncUserType)
    totalusers=graphene.Field(TotalUserType)


    @login_required
    def resolve_transaction(self, info, fromdate, todate):
        if fromdate and todate:
            return DailyTransaction.getDatabetweenspecifieddates(fromdate,todate)
        else:
            return DailyTransaction.objects.all()

    @login_required
    def resolve_fifteendaytd(self,info):
              
        td=DailyTransaction()
        return td.fifteendaydata()
    
    @login_required
    def resolve_todaydata(self, info):
        return DailyTransaction.todaydata()

    @login_required
    def resolve_incuserdata(self, info):
        return IncrementalUser.getfifteenddaydata()

    @login_required
    def resolve_totalusers(self, info):
        print("Here")
        return TotalUsers.getTotalUser()


class UpdateFromFile(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    @login_required
    def mutate(self, info, file, **kwargs):
        
        xl=XLSheet(xl=file['originFileObj'])
        xl.save()
        DailyTransaction.createEntry(file)

        return UpdateFromFile(success=True)

class AddIncrementalUsers(graphene.Mutation):
    class Arguments:
        date=graphene.Date(required=True)
        upiinc=graphene.Int(required=True)
        mbinc=graphene.Int(required=True)

    success=graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, date, upiinc, mbinc):
        res=None
        try:
            res=IncrementalUser.objects.get(date=date)
        except:
            pass
        if res:
            raise Exception("Entry for this date Already found. if you have made some mistake, then please correct it from admin panel")

        incObj=IncrementalUser()
        incObj.createInc(date,mbinc,upiinc)
        TotalUsers.updateUsers(incObj.inc_mbUsers, incObj.inc_upiUsers)
        return AddIncrementalUsers(success=True)

class Mutation(graphene.ObjectType):
    upload=UpdateFromFile.Field()
    addIncrementalUser=AddIncrementalUsers.Field()