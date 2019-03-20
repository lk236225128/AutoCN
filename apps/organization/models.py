from django.db import models
from autoCN.settings import MEDIA_ROOT
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

def upload_to(instance, filename):
    return '/'.join([MEDIA_ROOT, '/yaml/',instance.project.project, filename])


# Create your models here.

class Department(models.Model):
    department = models.CharField(verbose_name='部门(英文)', max_length=100)
    departmentName = models.CharField(verbose_name='部门(中文)', max_length=100, default='')

    class Meta:
        verbose_name = "部门管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.department


class Env(models.Model):
    project = models.ForeignKey("Project", verbose_name='所属项目', on_delete=models.CASCADE)
    env = models.CharField(verbose_name=u"环境(英文)", max_length=100)
    envName = models.CharField(verbose_name=u"环境(中文)", max_length=100, default='')
    baseUrl = models.URLField(verbose_name=u"默认链接", max_length=200, default='')

    class Meta:
        verbose_name = "环境管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.env


class Project(models.Model):
    department = models.ForeignKey("Department", verbose_name=u"所属部门", on_delete=models.CASCADE)
    project = models.CharField(verbose_name=u"项目(英文)", max_length=100)
    projectName = models.CharField(verbose_name=u"项目(中文)", max_length=100, default='')

    class Meta:
        verbose_name = "项目管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.project


class Platform(models.Model):
    project = models.ForeignKey("Project", verbose_name='所属项目', on_delete=models.CASCADE)
    platform = models.CharField(verbose_name=u"运行平台(英文)", max_length=20)
    platformName = models.CharField(verbose_name=u"运行平台(中文)", max_length=20)

    class Meta:
        verbose_name = "平台管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.platform


class RunType(models.Model):
    project = models.ForeignKey("Project", verbose_name='所属项目', on_delete=models.CASCADE)
    runType = models.CharField(verbose_name='执行类型(英文)', max_length=100, null=True)  # 1手动执行,2每日构建,3脚本
    runTypeName = models.CharField(verbose_name='执行类型(中文)', max_length=100, null=True)

    class Meta:
        verbose_name = "执行方式"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.runType


class Case(models.Model):
    project = models.ForeignKey("Project", verbose_name='所属项目', on_delete=models.CASCADE)
    caseName = models.FileField(upload_to=upload_to, verbose_name='用例文件', null=True)

    class Meta:
        verbose_name = "测试用例"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.caseName)


@receiver(pre_delete, sender=Case)
def mymodel_delete(sender, instance, **kwargs):
    instance.caseName.delete(False)