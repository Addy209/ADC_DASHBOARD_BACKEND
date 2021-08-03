from django.db import models

# Create your models here.
class Month(models.Model):
    code=models.PositiveSmallIntegerField(primary_key=True)
    month=models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.code)+" => "+self.month

class Year(models.Model):
    year=models.PositiveSmallIntegerField(primary_key=True)

    def __str__(self) -> str:
        return str(self.year)

class Module(models.Model):
    code=models.PositiveSmallIntegerField(primary_key=True)
    module=models.CharField(max_length=50)

    def __str__(self) -> str:
        return str(self.code)+" => "+self.module

class Priority(models.Model):
    code=models.PositiveSmallIntegerField(primary_key=True)
    priority=models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.code)+" => "+self.priority