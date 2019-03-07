from django.db import models
import datetime


# Create your models here.


# 對應數據庫中的一張表
class CaseResult(models.Model):
    id = models.AutoField('ID', primary_key=True)
    department = models.CharField(verbose_name='部门', choices=(("newCar", "新车"), ("usedCar", "中古车")), max_length=10,
                                  default='')
    taskid = models.IntegerField(verbose_name='taskID号', default=0)
    runType=models.CharField(verbose_name='执行类型', max_length=25,null=True, default='手动执行')
    success = models.BooleanField(verbose_name='执行结果')
    stat_testsRun = models.IntegerField(verbose_name='執行用例數')
    stat_successes = models.IntegerField(verbose_name='成功用例數')
    stat_failures = models.IntegerField(verbose_name='失敗用例數')
    stat_skipped = models.IntegerField(verbose_name='跳過用例數')
    stat_errors = models.IntegerField(verbose_name='Error用例數')
    passrate = models.FloatField(verbose_name='通过率', null=True)

    stat_expectedFailures = models.IntegerField(verbose_name='斷言失敗用例', null=True)  #
    stat_unexpectedSuccesses = models.IntegerField(verbose_name='', null=True)  #

    time_startat = models.FloatField(verbose_name='開始時間')
    duration = models.FloatField(verbose_name='耗時')
    httpRunner_version = models.CharField(verbose_name='HttpRunner版本', max_length=40)
    python_version = models.CharField(verbose_name='python版本', max_length=20)
    platform = models.CharField(verbose_name='平台',max_length=20,default='')

    case_reports = models.OneToOneField("HtmlReport", on_delete=models.CASCADE, null=True)
    notesCategory = models.CharField(max_length=100, null=True)
    # caseDetails = models.ForeignKey("CaseDetail", on_delete=models.CASCADE, null=True)

    notes = models.TextField(verbose_name='備註', null=True)
    isnotes = models.BooleanField(verbose_name='是否备注', default=False)
    # TODO 改为外键
    env = models.CharField(verbose_name='測試環境', max_length=30, null=True,default='testEnv')
    reporturl = models.CharField(verbose_name='报告链接', max_length=80, null=True)

    class Meta:
        verbose_name = "執行結果"
        verbose_name_plural = verbose_name
        db_table = 'CaseResult'

    def __str__(self):
        # <CaseResult:(id,success)>
        return "<Book:{id},{success}>".format(id=self.id, success=self.success)


# 生成遷移腳本文件
# python manage.py makemigrations

# 將遷移腳本文件映射到數據庫中
# python manage.py migrate



class HtmlReport(models.Model):
    details = models.TextField(verbose_name='结果详情', null=True)

    class Meta:
        verbose_name = "测试报告"
        verbose_name_plural = verbose_name
        db_table = 'HtmlReport'

    def __str__(self):
        return self.details


class CaseDetail(models.Model):
    department = models.CharField(verbose_name='部门', choices=(("newCar", "新车"), ("usedCar", "中古车")), max_length=10,
                                  default='')
    env = models.CharField(verbose_name='測試環境', max_length=30, null=True)
    case_name = models.CharField(max_length=100, null=True)
    case_success = models.BooleanField(verbose_name='detail执行结果')
    case_stat_testsRun = models.IntegerField(verbose_name='detail執行用例數')
    case_stat_successes = models.IntegerField(verbose_name='detail成功用例數')
    case_stat_failures = models.IntegerField(verbose_name='detail失敗用例數')
    case_stat_skipped = models.IntegerField(verbose_name='detail跳過用例數')
    case_stat_errors = models.IntegerField(verbose_name='detailError用例數')
    case_stat_expectedFailures = models.IntegerField(verbose_name='detail斷言失敗用例', null=True)  #
    case_stat_unexpectedSuccesses = models.IntegerField(verbose_name='', null=True)  #

    case_time_startat = models.FloatField(verbose_name='開始時間')
    case_time_startmonth = models.ImageField(verbose_name='用例执行月份', null=True)
    case_time_startyear = models.ImageField(verbose_name='用例执行年份', null=True)
    case_duration = models.FloatField(verbose_name='耗時')
    caseResult = models.ForeignKey("CaseResult", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "执行详情"
        verbose_name_plural = verbose_name
        db_table = 'CaseDetail'

    def __str__(self):
        return "<caseResult:{caseResult}>".format(caseResult=self.caseResult)


class NotesCategory(models.Model):
    notesCategory = models.CharField(max_length=100)

    class Meta:
        verbose_name = "备注类别"
        verbose_name_plural = verbose_name
        db_table = 'notesCategory'

    def __str__(self):
        return self.notesCategory


class Env(models.Model):
    env = models.CharField(max_length=100)
    envName = models.CharField(max_length=100,default='')
    # caseResult = models.ForeignKey("CaseResult", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "环境管理"
        verbose_name_plural = verbose_name
        db_table = 'Env'

    def __str__(self):
        return self.env


class Platform(models.Model):
    # platform = models.CharField(verbose_name=u"平台",
    #                             choices=(("iOS", "iOS"), ("Android", "Android"), ("H5", "触屏"), ("PC", "PC")),
    #                             max_length=20,default='PC')
    platform = models.CharField(verbose_name=u"平台",max_length=20,default='PC')

    class Meta:
        verbose_name = "平台管理"
        verbose_name_plural = verbose_name
        db_table = 'Platform'

    def __str__(self):
        return self.platform

class Department(models.Model):
    department = models.CharField(max_length=100)
    departmentName = models.CharField(max_length=100,default='')

    class Meta:
        verbose_name = "部门管理"
        verbose_name_plural = verbose_name
        db_table = 'Department'

    def __str__(self):
        return self.department

# 對應數據庫中的一張表
class Article(models.Model):
    articleName = models.CharField(max_length=50, null=False, verbose_name="文章标题")
    author = models.CharField(max_length=50, null=False, verbose_name="作者")
    add_time = models.DateTimeField(default=datetime.datetime.now, verbose_name="添加时间 ")
    aritcleDescription = models.TextField(verbose_name="文章简述", null=True)
    aritcleContent = models.TextField(verbose_name="文章内容")
    articleImg = models.ImageField(upload_to="static/img/%Y/%m", verbose_name="封面图", max_length=100)

    class Meta:
        verbose_name = "文章管理"
        verbose_name_plural = verbose_name
        db_table = 'Article'

    def __str__(self):
        return self.articleName


class RunType(models.Model):
    runType=models.CharField(verbose_name='执行类型', max_length=25,null=True, default='手动执行')  # 1手动执行,2每日构建,3脚本

    class Meta:
        verbose_name = "执行方式"
        verbose_name_plural = verbose_name
        db_table = 'RunType'

    def __str__(self):
        return self.runType