import xadmin

from .models import NotesCategory,CaseResult,CaseDetail

class ArticleAdmin(object):
    list_display=['articleName','author','add_time','articleImg']
#
# class DepartmentAdmin(object):
#     list_display=['department','departmentName']
#
# class PlatformAdmin(object):
#     list_display=['id','platform']
#
# class EnvAdmin(object):
#     list_display=['env','envName']

class NotesCategoryAdmin(object):
    list_display=['notesCategory']

# class RunTypeAdmin(object):
#     list_display=['runType']

class CaseResultAdmin(object):
    list_display=['id','department','taskid','runType','success','stat_testsRun','stat_successes','stat_failures','stat_skipped','stat_errors','passrate','stat_expectedFailures','stat_unexpectedSuccesses','time_startat','duration','httpRunner_version','python_version','platform','notesCategory','notes','isnotes','env','reporturl']

class CaseDetailAdmin(object):
    list_display=['id','department','env','case_name','case_success','case_stat_testsRun','case_stat_successes','case_stat_failures','case_stat_skipped','case_stat_errors','case_stat_expectedFailures','case_stat_unexpectedSuccesses','case_time_startat','case_time_startmonth','case_time_startyear','case_duration','caseResult']

# xadmin.site.register(Department,DepartmentAdmin)
# xadmin.site.register(Platform,PlatformAdmin)
# xadmin.site.register(Env,EnvAdmin)
xadmin.site.register(NotesCategory,NotesCategoryAdmin)
# xadmin.site.register(RunType,RunTypeAdmin)
xadmin.site.register(CaseResult,CaseResultAdmin)
xadmin.site.register(CaseDetail,CaseDetailAdmin)