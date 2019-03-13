from django.shortcuts import render
from django.views.generic import View
from .models import Article
import markdown

from organization.models import Project, Department


# Create your views here.



class articleDetailView(View):
    def get(self, request, articleID):
        department = request.GET.get('department', None)
        project = request.GET.get('project', None)

        if project:
            project = Project.objects.get(project=project)
        else:
            project = department.project_set.first()

        if department:
            department = Department.objects.get(department=department)
            projectList = department.project_set.all()

        article = Article.objects.get(pk=articleID)
        article.aritcleContent = markdown.markdown(article.aritcleContent, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        return render(request, "articleDetail.html",
                      context={"article": article, "project": project, "department": department,
                               "projectList": projectList})


class articleListView(View):
    def get(self, request):
        department = request.GET.get('department', None)

        project = request.GET.get('project', None)
        if project:
            project = Project.objects.get(project=project)
        else:
            project = department.project_set.first()

        if department:
            department = Department.objects.get(department=department)
            projectList = department.project_set.all()

        article = Article.objects.all()
        return render(request, "articleList.html",
                      context={"articleList": article, "project": project, "department": department,
                               "projectList": projectList})
