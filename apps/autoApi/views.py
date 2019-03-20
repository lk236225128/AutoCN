# coding=utf-8

from django.shortcuts import render
from .models import CaseResult
from httprunner import HttpRunner
from django.http import HttpResponse
from .models import CaseResult, HtmlReport, CaseDetail, NotesCategory
from organization.models import Env, Platform, RunType, Project, Department
import json
import time
from django.utils.safestring import mark_safe
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Sum
import os
from autoCN.settings import YAML_ROOT
from utils.mixin_utils import LoginRequiredMixin
from users.models import UserProfile

# ok
class dashboardView(LoginRequiredMixin,View):
    def get(self, request):
        resultList = CaseResult.objects.all()
        notesCategory = NotesCategory.objects.all()

        department = request.GET.get('department', None)
        project = request.GET.get('project', None)

        try:
            department = Department.objects.get(department=department)
        except Exception as e:
            return render(request, "errorPage.html",context={"message":"department不存在"})

        if project == None:
            project = department.project_set.first()
        else:
            project = Project.objects.get(project=project)

        projectList = department.project_set.all()
        resultList = resultList.filter(project=project).order_by("-time_startat")

        return render(request, "dashboard.html",
                      context={'resultList': resultList,
                               'notesCategory': notesCategory,
                               'project': project,
                               'projectList': projectList,
                               'department': department}
                      )


# OK
class ReturnRateView(View):
    def get(self, request):

        caseResults = CaseResult.objects.all()
        department = request.GET.get('department')
        department = Department.objects.get(department=department)
        project = request.GET.get('project')

        if department:
            caseResults = caseResults.filter(project=project)
        result = []
        for caseResult in caseResults:
            rate = caseResult.passrate * 100
            result.append({"id": caseResult.id, "rate": format(rate, '.2f')})

        return HttpResponse(json.dumps(result))


class failReasonView(LoginRequiredMixin,View):
    def get(self, request):
        # 失败原因汇总
        env = request.GET.get('env', None)

        department = request.GET.get('department', None)
        project = request.GET.get('project', None)

        try:
            department = Department.objects.get(department=department)
        except Exception as e:
            return render(request, "errorPage.html",context={"message":"department不存在"})

        try:
            project = Project.objects.get(project=project)
        except Exception as e:
            return render(request, "errorPage.html",context={"message":"project不存在"})

        if env:
            env = Env.objects.get(env=env)
        else:
            env = project.env_set.first()

        envList = project.env_set.all()

        projectList = department.project_set.all()
        # failResultList = CaseResult.objects.all()

        failResultList = CaseResult.objects.filter(notesCategory__isnull=False).filter(department=department,env=env).order_by('-id')

        nowYear = time.strftime("%Y", time.localtime())
        nowMonth = time.strftime("%m", time.localtime())

        allAnalysis = CaseDetail.objects.all()
        allAnalysis = allAnalysis.filter(department=department,
                                         env=env,
                                         case_time_startyear=nowYear,
                                         case_time_startmonth=nowMonth).values_list('case_name').annotate(
                Sum('case_stat_testsRun'), Sum('case_stat_successes'), Sum('case_stat_failures')).order_by('case_name')

        return render(request, "failReason.html",
                      context={'allFailResultList': failResultList,
                               "department": department,
                               "env": env,
                               "AnalysisList": allAnalysis,
                               "nowMonth": nowMonth,
                               "nowYear": nowYear,
                               "project": project,
                               "projectList": projectList,
                               "envList": envList})

class RunPageView(View):
    def get(self, request):
        department = request.GET.get('department', None)
        project = request.GET.get('project', None)

        try:
            department = Department.objects.get(department=department)
        except Exception as e:
            return render(request, "errorPage.html",context={"message":"department不存在"})

        try:
            project = Project.objects.get(project=project)
        except Exception as e:
            return render(request, "errorPage.html",context={"message":"project不存在"})

        projectList = department.project_set.all()

        envList = project.env_set.all()
        platformList = project.platform_set.all()
        runTypeList = project.runtype_set.all()

        dirList = []
        fileList = []
        yamlpath = os.path.join(YAML_ROOT, str(project))
        for root, dirs, files in os.walk(yamlpath):
            if dirs:
                for y in dirs:
                    dirPath = root + '/' + y
                    if str(project) in dirPath:
                        dirList.append({"dirPath": dirPath})
            if files:
                for x in files:
                    fileName = x
                    filePath = root + '/' + x
                    if str(project) in filePath:
                        fileList.append({"fileName": fileName, "filePath": filePath, "project": project})
                    elif str(project) in filePath:
                        fileList.append({"fileName": fileName, "filePath": filePath, "project": project})
        return render(request, "runCase.html",
                      context={"dirList": dirList, "fileList": fileList, "department": department, "envList": envList,
                               "platformList": platformList, "runTypeList": runTypeList, "project": project,
                               "projectList": projectList})


class RunCaseView(LoginRequiredMixin,View):
    def post(self, request):
        # department = request.GET.get('department', "8891")
        project = request.POST.get("project", "usedCar")
        department=Project.objects.get(project=project).department
        platform = request.POST.get('platform', "PC")
        runPath = request.POST.get('runPath')
        runType = request.POST.get('runtype')
        env = request.POST.get('env')
        baseUrl = request.POST.get('baseUrl','')
        # baseUrl=Env.objects.get(env=env).baseUrl
        cookie = request.POST.get('cookie')
        runpeople=str(request.user.username)

        time_startat = RunCase(self, department, project, baseUrl, runPath, runType, env, platform, cookie,runpeople)

        case = CaseResult.objects.filter(time_startat=time_startat).first().case_reports

        return render(request, "view_report.html", context={'detail': mark_safe(case)})

#http://172.16.3.204:8000/jenkinsRunCase/?project=usedCar&platform=Android&runType=hand&env=test&jobnumber=10666&cookie=task-1001009
class JenkinsRunCaseView(View):
    def get(self, request):
        project = request.GET.get("project", "usedCar")
        department=Project.objects.get(project=project).department
        platform = request.GET.get('platform', "")
        #默认执行所有用例
        yamlpath = os.path.join(YAML_ROOT, str(project))
        runPath = request.GET.get('runPath',yamlpath)
        runType = request.GET.get('runType')
        runType=str(RunType.objects.get(runType=runType).runTypeName)
        env = request.GET.get('env','')
        baseUrl=Env.objects.get(env=env).baseUrl

        env=str(Env.objects.get(env=env).envName)
        #自动根据env选择baseUrl
        cookie = request.GET.get('cookie','')
        jobnumber = request.GET.get('jobnumber')
        runpeople=str(UserProfile.objects.get(jobnumber=jobnumber).username)

        time_startat = RunCase(self, department, project, baseUrl, runPath, runType, env, platform, cookie,runpeople)
        # case = CaseResult.objects.filter(time_startat=time_startat).first().case_reports
        # return render(request, "view_report.html", context={'detail': mark_safe(case)})
        return HttpResponse('{"status":"success", "msg":"run success"}', content_type='application/json')


# 调用HttpRunner执行用例,并存入数据库
def RunCase(self, department, project, baseUrl, runPath, runType, env, platform, cookie,runpeople):

    override_mapping = {
            "base_url": baseUrl,
            "cookie": cookie
    }
    runner = HttpRunner(failfast=False);
    runner.run(runPath, mapping=override_mapping);
    summary = runner.summary;
    success = summary["success"]
    stat_testsRun = summary["stat"]["testsRun"]
    stat_successes = summary["stat"]["successes"]
    passrate = stat_successes / stat_testsRun
    stat_failures = summary["stat"]["failures"]
    stat_errors = summary["stat"]["errors"]
    stat_skipped = summary["stat"]["skipped"]
    time_startat = summary["time"]["start_at"]
    duration = summary["time"]["duration"]
    httpRunner_version = summary["platform"]["httprunner_version"]
    python_version = summary["platform"]["python_version"]
    platform = platform
    env = env
    department = department
    project = project
    detail = summary

    # 生成测试报告
    report = runner.gen_html_report(
            html_report_name="",
            html_report_template="./templates/report_template2.html"
    )

    with open(report, encoding='utf-8') as stream:
        case_reports = stream.read()

    htmlReport = HtmlReport(details=case_reports)
    htmlReport.save()

    reporturl = report
    # 保存执行结果
    caseResult = CaseResult(success=success,
                            stat_testsRun=stat_testsRun,
                            stat_successes=stat_successes,
                            stat_failures=stat_failures,
                            stat_errors=stat_errors,
                            stat_skipped=stat_skipped,
                            passrate=passrate,
                            runType=runType,
                            time_startat=time_startat,
                            duration=duration,
                            httpRunner_version=httpRunner_version,
                            python_version=python_version,
                            case_reports=htmlReport,
                            platform=platform,
                            env=env,
                            reporturl=reporturl,
                            department=department,
                            project=project,
                            cookie=cookie,
                            runpeople=runpeople);
    caseResult.save()
    if (len(detail["details"]) > 0):

        for i in range(len(detail["details"])):
            details_name = detail["details"][i]["name"]
            details_success = detail["details"][i]["success"]
            details_stat_testsRun = detail["details"][i]["stat"]["testsRun"]
            details_stat_successes = detail["details"][i]["stat"]["successes"]
            details_stat_failures = detail["details"][i]["stat"]["failures"]
            details_stat_skipped = detail["details"][i]["stat"]["skipped"]
            details_stat_errors = detail["details"][i]["stat"]["errors"]
            details_stat_expectedFailures = detail["details"][i]["stat"]["expectedFailures"]
            details_stat_unexpectedSuccesses = detail["details"][i]["stat"]["unexpectedSuccesses"]
            department = department
            project = project
            env = env
            case_time_startmonth = time.strftime("%m", time.localtime())
            case_time_startyear = time.strftime("%Y", time.localtime())

            details_time_start_at = detail["details"][i]["time"]["start_at"]
            details_duration = detail["details"][i]["time"]["duration"]

            # 保持各模块执行详情
            caseDetail = CaseDetail(department=department,
                                    project=project,
                                    env=env,
                                    case_name=details_name,
                                    case_success=details_success,
                                    case_stat_testsRun=details_stat_testsRun,
                                    case_stat_successes=details_stat_successes,
                                    case_stat_failures=details_stat_failures,
                                    case_stat_skipped=details_stat_skipped,
                                    case_stat_errors=details_stat_errors,
                                    case_stat_expectedFailures=details_stat_expectedFailures,
                                    case_stat_unexpectedSuccesses=details_stat_unexpectedSuccesses,
                                    case_time_startat=details_time_start_at,
                                    case_duration=details_duration,
                                    case_time_startmonth=case_time_startmonth,
                                    case_time_startyear=case_time_startyear)
            caseDetail.caseResult = caseResult
            caseDetail.save()
        return time_startat

    else:
        return time_startat


class reportDetailView(View):
    def get(self, request, reportID):
        case = CaseResult.objects.get(pk=reportID).case_reports
        return render(request, "view_report.html", context={'detail': mark_safe(case)})


class addNotesView(LoginRequiredMixin,View):
    def get(self, request):
        pass

    def post(self, request, noteID):
        notes = request.POST.get("notes", "")
        notesCategory = request.POST.get("notesCategory", "")
        case = CaseResult.objects.get(pk=noteID)
        case.notes = notes
        case.notesCategory = notesCategory
        case.isnotes = 1
        case.save()
        return HttpResponse('{"status":"success", "msg":"添加成功"}', content_type='application/json')


class failReportView(View):
    def get(self, request, department, env):
        result = []

        notesCategory = NotesCategory.objects.all()
        for Category in notesCategory:
            resultNum = CaseResult.objects.filter(notesCategory=Category.notesCategory, department=department,
                                                  env=env).count();

            result.append({"notesCategory": Category.notesCategory, "resultNum": resultNum})

        return HttpResponse(json.dumps(result))

    def post(self, request, noteID):
        pass


class caseListView(LoginRequiredMixin,View):
    def get(self, request):
        department = request.GET.get('department', None)
        project = request.GET.get('project', None)

        try:
            department = Department.objects.get(department=department)
        except Exception as e:
            return render(request, "errorPage.html",context={"message":"department不存在"})

        try:
            project = Project.objects.get(project=project)
        except Exception as e:
            return render(request, "errorPage.html",context={"message":"project不存在"})

        projectList = department.project_set.all()

        fileList = []
        yamlpath = os.path.join(YAML_ROOT, str(project))
        for root, dirs, files in os.walk(yamlpath):
            if files:
                for x in files:
                    fileName = x
                    filePath = root + '/' + x
                    if str(project) in filePath:
                        fileList.append({"fileName": fileName, "filePath": filePath})
        return render(request, "caseList.html",
                      context={"fileList": fileList, "department": department, "project": project,
                               "projectList": projectList})


class caseEditorView(LoginRequiredMixin,View):
    def get(self, request):
        department = request.GET.get('department', None)
        project = request.GET.get('project', None)

        try:
            department = Department.objects.get(department=department)
        except Exception as e:
            return render(request, "errorPage.html",context={"message":"department不存在"})

        if project == None:
            project = department.project_set.first()
        else:
            project = Project.objects.get(project=project)

        projectList = department.project_set.all()

        casePath = request.GET.get("casePath")
        with open(casePath, encoding='utf-8') as stream:
            caseDetail = stream.read()

        return render(request, "caseEditor.html",
                      context={"caseDetail": caseDetail, "casePath": casePath, "project": project,
                               "department": department, "projectList": projectList})

    def post(self, request):
        casePath = request.GET.get("casePath")
        caseDetail = request.POST.get("caseDetail")
        with open(casePath, 'w', encoding='utf-8') as stream:
            stream.write(caseDetail)
        return render(request, "caseEditor.html", context={"caseDetail": caseDetail, "status_code": '修改成功'})


if __name__ == '__main__':
    pass
