from django.db.models import fields
import graphene
from graphene_django import DjangoObjectType
from .models import *
from graphql_jwt.decorators import login_required
import graphql_jwt
from graphene_file_upload.scalars import Upload
import datetime

class TransactionType(DjangoObjectType):
    class Meta:
        model=DailyTransaction
        fields='__all__'


class IncUserType(DjangoObjectType):
    class Meta:
        model=IncrementalUser
        fields="__all__"
        
class TotalUserType(DjangoObjectType):
    class Meta:
        model=TotalUser
        fields="__all__"

# ("date","mb_fintxns","mb_nonfintxns","mb_totaltxn","mb_td","mb_td_percent","mb_bd",
#                 "upi_fintxns","upi_nonfintxns","upi_totaltxn","upi_td","upi_td_percent","upi_bd",
#                 "imps_totaltxn","imps_td","imps_td_percent","imps_bd")

class Query(graphene.ObjectType):
    transaction=graphene.List(TransactionType, fromdate=graphene.Date(required=False), todate=graphene.Date(required=False))
    fifteendaytd=graphene.List(TransactionType)
    todaydata=graphene.Field(TransactionType)
    incuserdata=graphene.List(IncUserType)
    totaluser=graphene.Field(TotalUserType)
    latestinc=graphene.Field(IncUserType)


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
    def resolve_totaluser(self, info):
        return TotalUser.objects.latest("date")
    
    @login_required
    def resolve_latestinc(self, info):
        return IncrementalUser.objects.latest("date")



class UpdateFromFile(graphene.Mutation):
    class Arguments:
        file = Upload(required=True)

    success = graphene.Boolean()

    @login_required
    def mutate(self, info, file, **kwargs):

        DailyTransaction.createEntry(file)

        return UpdateFromFile(success=True)

class AddIncrementalUsers(graphene.Mutation):
    class Arguments:
        date=graphene.Date(required=True)
        upiinc=graphene.Int(required=True)
        mbinc=graphene.Int(required=True)

    totalusers=graphene.Field(TotalUserType)

    @classmethod
    @login_required
    def mutate(cls, root, info, date, upiinc, mbinc):
        res=None
        try:
            res=IncrementalUser.objects.get(date=date)
        except:
            pass
        if res:
            raise Exception("Entry for this date found. if you want to update data then please do it from admin panel|")

        totaluser=TotalUser.objects.latest("date")
        test=totaluser.date+datetime.timedelta(1)==date
        if not test:
            raise Exception(f"Inconsitent Data, Last Date For which Total User Entry Found is {totaluser.date} Please add data for {totaluser.date+datetime.timedelta(1)}|")
        
        mb=mbinc-totaluser.mb
        upi=upiinc-totaluser.upi
        incObj=IncrementalUser()
        incObj.createInc(date,mb,upi)
        tot=TotalUser()
        tot.saveData(date, mbinc, upiinc)
        
        return AddIncrementalUsers(totalusers=tot)

class Mutation(graphene.ObjectType):
    upload=UpdateFromFile.Field()
    addIncrementalUser=AddIncrementalUsers.Field()