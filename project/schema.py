from django.db.models import fields
import graphene
from graphene.types.scalars import String
from graphene_django import DjangoObjectType
from .models import *
from graphql_jwt.decorators import login_required
import graphql_jwt
from graphene_file_upload.scalars import Upload
from django.shortcuts import get_object_or_404

class ProjectType(DjangoObjectType):
    class Meta:
        model=Project
        fields='__all__'

class UploadDocumentType(DjangoObjectType):
    class Meta:
        model=uploadedDocument
        fields='__all__'

class Query(graphene.ObjectType):
    allproject=graphene.List(ProjectType)
    project=graphene.Field(ProjectType, id=graphene.ID(required=True))
    documents=graphene.List(UploadDocumentType, project=graphene.ID(required=True))
    counts=graphene.types.json.JSONString()
    deadlineProjects=graphene.List(ProjectType)

    def resolve_allproject(self, info):
        return Project.objects.all().order_by('livedate')

    def resolve_project(self, info, id):
        return Project.objects.get(id=id)
    
    def resolve_documents(self, info, project):
        return uploadedDocument.objects.filter(project=project)

    def resolve_counts(self, info):
        return Project.getCounts()
    
    def resolve_deadlineProjects(self, info):
        return Project.deadlineProjects()



class createProject(graphene.Mutation):
    class Arguments:
        module=graphene.ID(required=True)
        name=graphene.String(required=True)
        description=graphene.String(required=True)
        priority=graphene.ID(required=True)
        requestedby=graphene.String(required=True)
        dev_com_date=graphene.Date(required=True)
        dev_completed=graphene.Boolean(required=True)
        test_start_date=graphene.Date(required=True)
        test_complete_date=graphene.Date(required=True)
        test_completed=graphene.Boolean(required=True)
        signoff=graphene.Boolean(required=True)
        livedate=graphene.Date(required=True)
        live=graphene.Boolean(required=True)
    
    project=graphene.Field(ProjectType)

    @classmethod
    def mutate(cls, root, info, module,name,description,priority,requestedby,dev_com_date,dev_completed, test_start_date,
                        test_complete_date, test_completed, signoff, livedate,live):
        project_obj=Project()
        project_obj.createProject(module,name,description,priority,requestedby,dev_com_date,dev_completed, test_start_date,
                        test_complete_date, test_completed, signoff, livedate,live)
        return createProject(project=project_obj)

class updateProject(graphene.Mutation):
    class Arguments:
        id=graphene.ID(required=True)
        module=graphene.ID(required=True)
        name=graphene.String(required=True)
        description=graphene.String(required=True)
        priority=graphene.ID(required=True)
        requestedby=graphene.String(required=True)
        dev_com_date=graphene.Date(required=True)
        dev_completed=graphene.Boolean(required=True)
        test_start_date=graphene.Date(required=True)
        test_complete_date=graphene.Date(required=True)
        test_completed=graphene.Boolean(required=True)
        signoff=graphene.Boolean(required=True)
        livedate=graphene.Date(required=True)
        live=graphene.Boolean(required=True)
    
    project=graphene.Field(ProjectType)

    @classmethod
    def mutate(cls, root, info, id, module,name,description,priority,requestedby,dev_com_date,dev_completed, test_start_date,
                        test_complete_date, test_completed, signoff, livedate,live):
        try:
            project_obj=get_object_or_404(Project, pk=id)
            project_obj.createProject(module,name,description,priority,requestedby,dev_com_date,dev_completed, test_start_date,
                            test_complete_date, test_completed, signoff, livedate,live)
            return updateProject(project=project_obj)

        except Exception as e:
            raise Exception(e)


class DocumentUpload(graphene.Mutation):
    class Arguments:
        project=graphene.ID(required=True)
        name=graphene.String(required=True)
        document=Upload(required=True)

    savedDocument=graphene.List(UploadDocumentType)

    @classmethod
    def mutate(cls, root, info, project,name,document):
        try:
            doc=uploadedDocument()
            doc.saveDocument(project,name,document['originFileObj'])
            doc=uploadedDocument.objects.filter(project=project)
            return DocumentUpload(savedDocument=doc)
        except Exception as e:
            raise Exception(e)

class Mutation(graphene.ObjectType):
    createProject=createProject.Field()
    updateProject=updateProject.Field()
    documentUpload=DocumentUpload.Field()

