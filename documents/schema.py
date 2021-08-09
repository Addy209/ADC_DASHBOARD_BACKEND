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

class FileType(DjangoObjectType):
    class Meta:
        model=File
        fields='__all__'

class Query(graphene.ObjectType):
    myfiles=graphene.List(FileType)
    sharedfiles=graphene.List(FileType)

    @login_required
    def resolve_myfiles(self, info):
        user=info.context.user
        print(user)
        return File.objects.filter(user=user).order_by("uploaded_at")

    @login_required
    def resolve_sharedfiles(self, info):
        user=info.context.user
        return File.objects.filter(~Q(user=user) & Q(private=False))    

class SaveFileMutation(graphene.Mutation):
    class Arguments:
        desc=graphene.String(required=True)
        file=Upload(required=True)
        private=graphene.Boolean(required=True)

    files=graphene.List(FileType)

    @classmethod
    @login_required
    def mutate(cls, root, info, desc, file, private):
        if file["size"]>10485760:
            raise Exception("42")
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
                raise Exception("02")
        except Exception as e:
            raise e

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
                print(not file.private)
                file.private= (not file.private)
                file.save()
                return PublishPrivate(success=True)
            else:
                raise Exception("Not Authorized")
        except Exception as e:
            raise e

class Mutation(graphene.ObjectType):
    savefile=SaveFileMutation.Field()
    deletefile=DeleteFileMutation.Field()
    publish=PublishPrivate.Field()