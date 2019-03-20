import xadmin

from .models import Department,Platform,Env,RunType,Project,Case

class DepartmentAdmin(object):
    list_display=['department','departmentName']

class PlatformAdmin(object):
    list_display=['project','platform','platformName']

class EnvAdmin(object):
    list_display=['project','env','envName','baseUrl']

class ProjectAdmin(object):
    list_display=['department','project','projectName']

class RunTypeAdmin(object):
    list_display=['project','runType','runTypeName']

class CaseAdmin(object):
    list_display=['project','caseName']


xadmin.site.register(Department,DepartmentAdmin)
xadmin.site.register(Platform,PlatformAdmin)
xadmin.site.register(Project,ProjectAdmin)
xadmin.site.register(Env,EnvAdmin)
xadmin.site.register(RunType,RunTypeAdmin)
xadmin.site.register(Case,CaseAdmin)