from typing import final
import graphene
from graphene.types.datetime import Date
from graphene_django import DjangoObjectType
from .models import *
from graphql_jwt.decorators import login_required
import graphql_jwt
import datetime
from graphene_file_upload.scalars import Upload
from utils.constants import *

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
            return Expenditure.objects.filter(module__code=module).order_by("date")


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
                            gst_percent,gst_amt,penalty,final_payment,invoice):
        if date<=datetime.date.today():
            bill=None
            try:
                bill=invoice['originFileObj']
            except:      
                pass
            expense=Expenditure()
            if bill:
                if invoice['size']>MAX_UPLOAD_SIZE:
                    raise Exception("Maximum Allowed File Size is {0}|".format(MAX_FILE_SIZE))
                expense.createExpenditure(date,module,description,fin_txn,
                            fin_rate,fin_cost,nonfin_txn,nonfin_rate,nonfin_cost,base_amt,
                            gst_percent,gst_amt,penalty,final_payment,bill)
            else:
                expense.createExpenditure(date,module,description,fin_txn,
                            fin_rate,fin_cost,nonfin_txn,nonfin_rate,nonfin_cost,base_amt,
                            gst_percent,gst_amt,penalty,final_payment)
            return CreateExpense(success=True)
        else:
            raise ValueError("Invalid Date Time Entry Found")

class CreateOtherExpense(graphene.Mutation):
    class Arguments:
        date=graphene.Date(required=True)
        module=graphene.ID(required=True)
        description=graphene.String(required=True)
        base_amt=graphene.Int(required=True)
        gst_percent=graphene.Float(required=True)
        gst_amt=graphene.Int(required=True)
        penalty=graphene.Int(required=True)
        final_payment=graphene.Int(required=True)
        invoice=Upload(required=False)

    success=graphene.Boolean()
    

    @classmethod
    @login_required
    def mutate(cls, root, info, date,module,description,base_amt,
                            gst_percent,gst_amt,penalty,final_payment,invoice):
        if date<=datetime.date.today():
            bill=None
            try:
                bill=invoice['originFileObj']

            except:      
                pass
            expense=Expenditure()
            if bill:
                if invoice['size']>MAX_UPLOAD_SIZE:
                    raise Exception("Maximum Allowed File Size is {0}".format(MAX_FILE_SIZE))
                expense.createOtherExpenditure(date,module,description,base_amt,
                            gst_percent,gst_amt,penalty,final_payment,bill)
            else:
                expense.createOtherExpenditure(date,module,description,base_amt,
                            gst_percent,gst_amt,penalty,final_payment)
            return CreateOtherExpense(success=True)
        else:
            raise ValueError("Invalid Date Time Entry Found")

class Mutation(graphene.ObjectType):
    create_expense=CreateExpense.Field()
    create_other_expense=CreateOtherExpense.Field()
