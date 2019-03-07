from django.shortcuts import render
from .models import CaseResult
from httprunner import HttpRunner
from django.http import HttpResponse
from .models import CaseResult, HtmlReport, CaseDetail, NotesCategory, Article,Env,Platform,RunType
import datetime
import json
import collections
import autoApi.autoUtil
import time
from django.utils.safestring import mark_safe
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Sum
import markdown
import os


class IndexView(View):
    def get(self, request):
        article = Article.objects.all()
        num = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

        return render(request, "index.html", context={"articleList": article, "num": num})


class dashboardView(View):
    def get(self, request):
        resultList = CaseResult.objects.all()
        notesCategory = NotesCategory.objects.all()

        department = request.GET.get('department', "usedCar")
        if department:
            resultList = resultList.filter(department=department).order_by("-time_startat")

        return render(request, "dashboard.html",
                      context={'resultList': resultList,
                               'notesCategory': notesCategory,
                               'department': department})


# TODO ?department=newCar
# TODO 前端时间未格式化

class failReasonView(View):
    def get(self, request):
        # 失败原因汇总

        failResultList = CaseResult.objects.all()
        department = request.GET.get('department', "usedCar")
        env = request.GET.get('env', "testEnv")

        failResultList = failResultList.filter(notesCategory__isnull=False).filter(department=department,
                                                                                   env=env).order_by('-id')

        nowYear = time.strftime("%Y", time.localtime())
        nowMonth = time.strftime("%m", time.localtime())

        allAnalysis = CaseDetail.objects.all()
        allAnalysis = allAnalysis.filter(department=department,
                                         env=env,
                                         case_time_startyear=nowYear,
                                         case_time_startmonth=nowMonth).values_list('case_name').annotate(
                Sum('case_stat_testsRun'), Sum('case_stat_successes'), Sum('case_stat_failures')).order_by('case_name')
        #     case_name = Analysis[0],case_stat_testsRun = Analysis[1],case_stat_successes = Analysis[2],case_stat_failures = Analysis[3]

        return render(request, "failReason.html",
                      context={'allFailResultList': failResultList,
                               "department": department,
                               "env": env,
                               "AnalysisList": allAnalysis,
                               "nowMonth": nowMonth,
                               "nowYear": nowYear})


# TODO ?department=usedCar&env=testEnv


class RunPageView(View):
    def get(self, request):
        department = request.GET.get('department', "usedCar")
        envList=Env.objects.all()
        platformList=Platform.objects.all()
        runTypeList=RunType.objects.all()

        dirList = []
        fileList = []
        for root, dirs, files in os.walk('/Users/luokai/autoProjects/autoCN/yaml'):
            if dirs:
                for y in dirs:
                    dirPath = root + '/' + y
                    if department in dirPath:
                        dirList.append({"dirPath": dirPath})
            if files:
                for x in files:
                    fileName = x
                    filePath = root + '/' + x
                    if department in filePath:
                        fileList.append({"fileName": fileName, "filePath": filePath, "department": department})
                    elif department in filePath:
                        fileList.append({"fileName": fileName, "filePath": filePath, "department": department})
        return render(request, "runCase.html",
                      context={"dirList": dirList, "fileList": fileList, "department": department,"envList":envList,"platformList":platformList,"runTypeList":runTypeList})


# TODO ?department=usedCar


class RunCaseView(View):
    def post(self, request, department):
        department = request.POST.get('department', "usedCar")
        platform = request.POST.get('platform', "PC")
        baseUrl = request.POST['baseUrl']
        runPath = request.POST['runPath']
        runType = request.POST['runtype']
        env = request.POST['env']
        task = request.POST['taskID']

        time_startat = RunCase(self, department, baseUrl, runPath, runType, env, platform, task)

        case = CaseResult.objects.filter(time_startat=time_startat).first().case_reports

        return render(request, "view_report.html", context={'detail': mark_safe(case)})

# 调用HttpRunner执行用例,并存入数据库
def RunCase(self, department, baseUrl, runPath, runType, env, platform, task):
    if env == 'testEnv':
        override_mapping = {
            "base_url": baseUrl,
            "task": task
        }
    elif env == 'onlineEnv':
        override_mapping = {
            "base_url": baseUrl,
            "task": ''
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
                            department=department);
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
            env = env
            case_time_startmonth = time.strftime("%m", time.localtime())
            case_time_startyear = time.strftime("%Y", time.localtime())

            details_time_start_at = detail["details"][i]["time"]["start_at"]
            details_duration = detail["details"][i]["time"]["duration"]

            # 保持各模块执行详情
            caseDetail = CaseDetail(department=department,
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


class ReturnRateView(View):
    def get(self, request, department):

        caseResults = CaseResult.objects.all()
        department = request.GET.get('department', "usedCar")
        if department:
            caseResults = caseResults.filter(department=department)
        result = []
        for caseResult in caseResults:
            rate = caseResult.passrate * 100
            result.append({"id": caseResult.id, "rate": format(rate, '.2f')})

        return HttpResponse(json.dumps(result))


class reportDetailView(View):
    def get(self, request, reportID):
        case = CaseResult.objects.get(pk=reportID).case_reports
        return render(request, "view_report.html", context={'detail': mark_safe(case)})


class addNotesView(View):
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


class caseListView(View):
    def get(self, request):
        fileList = []
        for root, dirs, files in os.walk('/Users/luokai/autoProjects/autoCN/yaml'):
            if files:
                for x in files:
                    fileName = x
                    filePath = root + '/' + x
                    if 'usedCar' in filePath:
                        fileList.append({"fileName": fileName, "filePath": filePath, "department": 'usedCar'})
                    elif 'newCar' in filePath:
                        fileList.append({"fileName": fileName, "filePath": filePath, "department": 'newCar'})
                    else:
                        fileList.append({"fileName": fileName, "filePath": filePath})

        return render(request, "caseList.html", context={"fileList": fileList})


class caseEditorView(View):
    def get(self, request):
        casePath = request.GET.get("casePath")
        # print(casePath)
        with open(casePath, encoding='utf-8') as stream:
            caseDetail = stream.read()
            # print(caseDetail)

        return render(request, "caseEditor.html", context={"caseDetail": caseDetail, "casePath": casePath})

    def post(self, request):
        casePath = request.GET.get("casePath")
        caseDetail = request.POST.get("caseDetail")
        with open(casePath, 'w', encoding='utf-8') as stream:
            stream.write(caseDetail)
        return render(request, "caseEditor.html", context={"caseDetail": caseDetail, "status_code": '修改成功'})


class articleDetailView(View):
    def get(self, request, articleID):
        article = Article.objects.get(pk=articleID)
        article.aritcleContent = markdown.markdown(article.aritcleContent, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        return render(request, "articleDetail.html", context={"article": article})


class articleListView(View):
    def get(self, request):
        article = Article.objects.all()
        return render(request, "articleList.html", context={"articleList": article})


if __name__ == '__main__':
    pass
