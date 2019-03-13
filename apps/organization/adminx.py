import xadmin

from .models import Department,Platform,Env,RunType,Project

class DepartmentAdmin(object):
    list_display=['department','departmentName']

class PlatformAdmin(object):
    list_display=['project','id','platform','platformName']

class EnvAdmin(object):
    list_display=['project','env','envName','baseUrl']

class ProjectAdmin(object):
    list_display=['department','project','projectName']

class RunTypeAdmin(object):
    list_display=['project','runType','runTypeName']

xadmin.site.register(Department,DepartmentAdmin)
xadmin.site.register(Platform,PlatformAdmin)
xadmin.site.register(Project,ProjectAdmin)
xadmin.site.register(Env,EnvAdmin)
xadmin.site.register(RunType,RunTypeAdmin)
