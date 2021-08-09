from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class File(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    desc=models.TextField()
    file=models.FileField(upload_to='files/%Y/%m/%d')
    type=models.CharField(max_length=255)
    size=models.PositiveBigIntegerField()
    private=models.BooleanField()
    uploaded_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
    
    def saveFile(self, user,desc,file,private):
        self.user=user
        self.name=file["name"]
        self.desc=desc
        self.file=file["originFileObj"]
        self.type=file["type"]
        self.size=file["size"]
        self.private=private
        self.save()
    