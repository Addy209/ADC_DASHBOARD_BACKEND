from django.db.models import fields
import graphene
from graphene_django import DjangoObjectType
from .models import *
from graphql_jwt.decorators import login_required
import graphql_jwt
from graphene_file_upload.scalars import Upload
from django.db.models import Q
import os
from django.conf import settings
from utils.constants import *

class FileType(DjangoObjectType):
    class Meta:
        model=File
        fields='__all__'

class Query(graphene.ObjectType):
    myfiles=graphene.List(FileType)
    sharedfiles=graphene.List(FileType)
    search=graphene.List(FileType ,text=graphene.String(required=True))

    @login_required
    def resolve_myfiles(self, info):
        user=info.context.user
        return File.objects.filter(user=user).order_by("uploaded_at")

    @login_required
    def resolve_sharedfiles(self, info):
        user=info.context.user
        return File.objects.filter(~Q(user=user) & Q(private=False)) 

    @login_required
    def resolve_search(self, info, text):
        res=[]
        user=info.context.user
        try:
            res=File.objects.filter((Q(name__icontains=text)|Q(desc__icontains=text)|Q(type__icontains=text)) & Q(private=False) & ~Q(user=user))
            userres=File.objects.filter((Q(name__icontains=text)|Q(desc__icontains=text)|Q(type__icontains=text)) & Q(user=user))
            res=res.union(userres).order_by("uploaded_at")
        except Exception as e:
            pass
        return res

class SaveFileMutation(graphene.Mutation):
    class Arguments:
        desc=graphene.String(required=True)
        file=Upload(required=True)
        private=graphene.Boolean(required=True)

    files=graphene.List(FileType)

    @classmethod
    @login_required
    def mutate(cls, root, info, desc, file, private):
        if file["size"]>MAX_UPLOAD_SIZE:
            raise Exception("Maximum Allowed File Size is {0}".format(MAX_FILE_SIZE))
        user=info.context.user
        file_obj=File()
        file_obj.saveFile(user, desc, file, private)
        file_obj=File.objects.filter(user=user).order_by("uploaded_at")
        return SaveFileMutation(files=file_obj)

class DeleteFileMutation(graphene.Mutation):
    class Arguments:
        id=graphene.ID(required=True)
        

    files=graphene.List(FileType)

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        user=info.context.user
        try:
            file=File.objects.get(id=id)
            if user==file.user:
                os.remove(os.path.join(settings.MEDIA_ROOT,str(file.file)))
                file.delete()
                file=File.objects.filter(user=user).order_by("uploaded_at")
                return DeleteFileMutation(files=file)
            else:
                raise Exception("You are not authorized to delete this file|")
        except Exception as e:
            raise Exception("Something went wrong while deleting the file|")

class PublishPrivate(graphene.Mutation):
    class Arguments:
        id=graphene.ID(required=True)
        

    success=graphene.Boolean()

    @classmethod
    @login_required
    def mutate(cls, root, info, id):
        user=info.context.user
        try:
            file=File.objects.get(id=id)
            if user==file.user:
                file.private= (not file.private)
                file.save()
                return PublishPrivate(success=True)
            else:
                raise Exception("You are not authorized to change visibility of the file|")
        except Exception as e:
            raise Exception("Something went wrong while changing visibility of the file|")

class Mutation(graphene.ObjectType):
    savefile=SaveFileMutation.Field()
    deletefile=DeleteFileMutation.Field()
    publish=PublishPrivate.Field()