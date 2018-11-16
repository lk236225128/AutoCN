from django.db import models


# Create your models here.

# 對應數據庫中的一張表
class CaseResult(models.Model):
    class Meta:
        verbose_name = "測試執行結果"
        db_table = 'CaseResult'

    id = models.AutoField('ID', primary_key=True)
    success = models.BooleanField('成功用例數')
    stat_testsRun = models.IntegerField('執行用例數')
    stat_successes = models.IntegerField('成功用例數')
    stat_failures = models.IntegerField('失敗用例數')
    stat_errors = models.IntegerField('Error用例數')
    stat_skipped = models.IntegerField('跳過用例數')
    start_datetime = models.CharField('開始時間', max_length=40)
    duration = models.FloatField('耗時')
    httpRunner_version = models.CharField('HttpRunner版本', max_length=40)
    python_version = models.CharField('python版本', max_length=20)
    platform = models.CharField('系統平臺', max_length=60)
    details = models.TextField('執行結果')
    notes = models.TextField('備註', null=True)
    env = models.CharField('測試環境', max_length=30, null=True)

    def __str__(self):
        # return self
        # <CaseResult:(id,success)>
        return "<Book:{id},{success}>".format(id=self.id, success=self.success)

# 生成遷移腳本文件
# python manage.py makemigrations

# 將遷移腳本文件映射到數據庫中
# python manage.py migrate
