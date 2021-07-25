from typing import final
import graphene
from graphene_django import DjangoObjectType
from .models import *
from graphql_jwt.decorators import login_required
import graphql_jwt
import datetime

class ExpenditureType(DjangoObjectType):
    class Meta:
        model=Expenditure
        fileds='__all__'

class Query(graphene.ObjectType):
    sixmonthdata=graphene.types.json.JSONString()

    def resolve_sixmonthdata(self,info):
        val=Expenditure.getSixMonthData()
        print(val)
        return val


class CreateExpense(graphene.Mutation):
    class Arguments:
        date=graphene.Date(required=True)
        module=graphene.Int(required=True)
        description=graphene.String(required=True)
        fin_txn=graphene.Int(required=True)
        fin_rate=graphene.Float(required=True)
        nonfin_txn=graphene.Int(required=True)
        nonfin_rate=graphene.Float(required=True)
        base_amt=graphene.Int(required=True)
        gst_percent=graphene.Float(required=True)
        gst_amt=graphene.Int(required=True)
        penalty=graphene.Int(required=True)
        final_payment=graphene.Int(required=True)

    success=graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, date,module,description,fin_txn,
                            fin_rate,nonfin_txn,nonfin_rate,base_amt,
                            gst_percent,gst_amt,penalty,final_payment):
        if date<=datetime.date.today():
            
            try:
                expense=Expenditure()
                expense.createExpenditure(date,module,description,fin_txn,
                            fin_rate,nonfin_txn,nonfin_rate,base_amt,
                            gst_percent,gst_amt,penalty,final_payment)
                return CreateExpense(success=True)
            except:      
                return CreateExpense(success=False)
        else:
            raise ValueError("Invalid Date Time Entry Found")

class Mutation(graphene.ObjectType):
    create_expense=CreateExpense.Field()
