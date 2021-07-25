from django.db import models
from django.db.models.aggregates import Count
from constants.models import *
import datetime
from django.db.models import Q
from django.db.models import Sum, Count

# Create your models here.

class Expenditure(models.Model):
    date=models.DateField()
    module=models.ForeignKey(Module, on_delete=models.CASCADE)
    description=models.CharField(max_length=255)
    fin_txn=models.PositiveBigIntegerField()
    fin_rate=models.FloatField()
    nonfin_txn=models.PositiveBigIntegerField()
    nonfin_rate=models.FloatField()
    base_amt=models.PositiveBigIntegerField()
    gst_percent=models.FloatField()
    gst_amt=models.PositiveBigIntegerField()
    penalty=models.PositiveBigIntegerField()
    final_payment=models.PositiveBigIntegerField()

    def __str__(self) -> str:
        return self.description

    def createExpenditure(self,date,module,description,fin_txn,
                            fin_rate,nonfin_txn,nonfin_rate,base_amt,
                            gst_percent,gst_amt,penalty,final_payment):
        self.date=date
        self.month=Month.objects.get(code=date.month)
        self.module=Module.objects.get(code=module)
        self.description=description
        self.fin_txn=fin_txn
        self.fin_rate=fin_rate
        self.nonfin_txn=nonfin_txn
        self.nonfin_rate=nonfin_rate
        self.base_amt=base_amt
        self.gst_percent=gst_percent
        self.gst_amt=gst_amt
        self.penalty=penalty
        self.final_payment=final_payment
        self.save()

    @classmethod
    def getSixMonthData(cls):
        latest=cls.objects.latest("date")
        old=latest.date-datetime.timedelta(180)
        val= cls.objects.values('module','date__month','date__year').filter(date__gte=old).annotate(Sum('final_payment')).order_by("date__month")
        res=[]
        for x in val:
            res.append(x)
        return res

        