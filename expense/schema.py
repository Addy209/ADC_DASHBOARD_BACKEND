from typing import final
import graphene
from graphene.types.datetime import Date
from graphene_django import DjangoObjectType
from .models import *
from graphql_jwt.decorators import login_required
import graphql_jwt
import datetime
from graphene_file_upload.scalars import Upload

class ExpenditureType(DjangoObjectType):
    class Meta:
        model=Expenditure
        fileds='__all__'

class Query(graphene.ObjectType):
    sixmonthdata=graphene.types.json.JSONString()
    expensedata=graphene.List(ExpenditureType, module=graphene.Int(required=True),fromDate=graphene.Date(required=False), toDate=graphene.Date(required=False))

    @login_required
    def resolve_sixmonthdata(self,info):
        return Expenditure.getSixMonthData()
    
    @login_required
    def resolve_expensedata(self, info, module,fromDate=None, toDate=None):
        if fromDate and toDate:
            return Expenditure.expenseData(module,fromDate,toDate)
        else:
            print("here")
            return Expenditure.objects.filter(module__code=module)


class CreateExpense(graphene.Mutation):
    class Arguments:
        date=graphene.Date(required=True)
        module=graphene.ID(required=True)
        description=graphene.String(required=True)
        fin_txn=graphene.Int(required=True)
        fin_rate=graphene.Float(required=True)
        fin_cost=graphene.Int(required=True)
        nonfin_txn=graphene.Int(required=True)
        nonfin_rate=graphene.Float(required=True)
        nonfin_cost=graphene.Int(required=True)
        base_amt=graphene.Int(required=True)
        gst_percent=graphene.Float(required=True)
        gst_amt=graphene.Int(required=True)
        penalty=graphene.Int(required=True)
        final_payment=graphene.Int(required=True)
        invoice=Upload(required=False)

    success=graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, date,module,description,fin_txn,
                            fin_rate,fin_cost,nonfin_txn,nonfin_rate,nonfin_cost,base_amt,
                            gst_percent,gst_amt,penalty,final_payment,invoice=None):
        print("I am here")
        if date<=datetime.date.today():
            
            try:
                invoice=invoice['originFileObj']
                expense=Expenditure()
                expense.createExpenditure(date,module,description,fin_txn,
                            fin_rate,fin_cost,nonfin_txn,nonfin_rate,nonfin_cost,base_amt,
                            gst_percent,gst_amt,penalty,final_payment,invoice)
                return CreateExpense(success=True)
            except:      
                return CreateExpense(success=False)
        else:
            raise ValueError("Invalid Date Time Entry Found")

class Mutation(graphene.ObjectType):
    create_expense=CreateExpense.Field()
