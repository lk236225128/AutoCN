from django.shortcuts import render
from .models import CaseResult
from httprunner import HttpRunner
from django.http import HttpResponse
from .models import CaseResult
import datetime
import json
import collections

# Create your views here.


def index(request):
    # # 添加一條數據到數據庫
    # caseResult = CaseResult(id=1)
    # caseResult.save()
    #
    # # 查詢: 查詢單條，若無結果則拋異常
    # case = caseResult.objects.get(pk=1)  # 根據主鍵查找
    #
    # # 查詢: 根據其它條件查詢
    # cases = caseResult.objects.filter(success='')  # 返回QuerySet列表
    # case2 = caseResult.objects.filter(success='').first()  # 獲取返回列表的第一個值
    #
    # # 修改
    # case = caseResult.objects.get(pk=1)
    # case.success = ''
    # case.save()
    #
    # # 刪除
    # # caseResult.delete()

    return render(request,"index.html")


def runTestCase(request):
    runner = HttpRunner(failfast=False);
    runner.run("./yaml/");
    summary = runner.summary;

    success = summary["success"]
    stat_testsRun = summary["stat"]["testsRun"]
    stat_successes = summary["stat"]["successes"]
    stat_failures = summary["stat"]["failures"]
    stat_errors = summary["stat"]["errors"]
    stat_skipped = summary["stat"]["skipped"]
    start_datetime = summary["time"]["start_at"],
    duration = summary["time"]["duration"]
    httpRunner_version = summary["platform"]["httprunner_version"]
    python_version = summary["platform"]["python_version"]
    platform = summary["platform"]["platform"]
    details = summary["details"]

    caseResult = CaseResult(success=success, stat_testsRun=stat_testsRun, stat_successes=stat_successes,
                            stat_failures=stat_failures, stat_errors=stat_errors, stat_skipped=stat_skipped,
                            start_datetime=start_datetime, duration=duration, httpRunner_version=httpRunner_version,
                            python_version=python_version, platform=platform, details=details);
    caseResult.save()
    report = runner.gen_html_report(
        html_report_name="",
        html_report_template="./templates/report_template.html"
    )
    print(report)
    return HttpResponse("run test Case")

def returnRate(request):
    # d=collections.OrderedDict()
    result=[{"id":1002011,"rate":99},{"id":1002012,"rate":90},{"id":1002013,"rate":96},{"id":1002014,"rate":88},{"id":1002015,"rate":70}]
    return HttpResponse(json.dumps(result))




if __name__ == '__main__':
    runTestCase();
