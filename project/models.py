from django.db import models
from constants.models import *
import datetime

# Create your models here.
class Project(models.Model):
    module=models.ForeignKey(Module, on_delete=models.CASCADE)
    name=models.CharField(max_length=511)
    description=models.TextField()
    priority=models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True)
    requestedby=models.CharField(max_length=255)
    dev_complete_date=models.DateField()
    dev_completed=models.BooleanField()
    test_start_date=models.DateField()
    test_complete_date=models.DateField()
    test_completed=models.BooleanField()
    signoff=models.BooleanField()
    livedate=models.DateField()
    live=models.BooleanField()

    def __str__(self) -> str:
        return self.name

    def createProject(self,module,name,description,priority,requestedby,dev_com_date,dev_completed, test_start_date,
                        test_complete_date, test_completed, signoff, livedate,live):
        self.module=Module.objects.get(code=module)
        self.name=name
        self.description=description
        self.priority=Priority.objects.get(code=priority)
        self.requestedby=requestedby
        self.dev_complete_date=dev_com_date
        self.dev_completed=dev_completed
        self.test_start_date=test_start_date
        self.test_complete_date=test_complete_date
        self.test_completed=test_completed
        self.signoff=signoff
        self.livedate=livedate
        self.live=live
        self.save()
    
    @classmethod
    def getCounts(cls):
        completed=cls.objects.filter(live=True).count()
        ongoing=cls.objects.filter(live=False).count()
        today=datetime.date.today()
        criticalDate=today+datetime.timedelta(15)
        critical=cls.objects.filter(livedate__range=(today, criticalDate), live=False).count()

        return {
            "completed":completed,
            "ongoing":ongoing,
            "critical":critical
        }
    
    @classmethod
    def deadlineProjects(cls):
        today=datetime.date.today()
        criticalDate=today+datetime.timedelta(15)
        critical=cls.objects.filter(livedate__range=(today, criticalDate), live=False).order_by('-priority__code')[0:5]
        return critical


class uploadedDocument(models.Model):
    project=models.ForeignKey(Project, related_name="project_document", on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    document=models.FileField(upload_to='projects/invoices/%Y/%m/%d')
    uploaded_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.project.name+"=>"+self.name

    def saveDocument(self,project,name,document):
        self.project=Project.objects.get(id=project)
        self.name=name
        self.document=document
        self.save()
