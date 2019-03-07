# Generated by Django 2.0 on 2018-12-07 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CaseDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_success', models.BooleanField(verbose_name='detail执行结果')),
                ('case_stat_testsRun', models.IntegerField(verbose_name='detail執行用例數')),
                ('case_stat_successes', models.IntegerField(verbose_name='detail成功用例數')),
                ('case_stat_failures', models.IntegerField(verbose_name='detail失敗用例數')),
                ('case_stat_skipped', models.IntegerField(verbose_name='detail跳過用例數')),
                ('case_stat_errors', models.IntegerField(verbose_name='detailError用例數')),
                ('case_stat_expectedFailures', models.IntegerField(null=True, verbose_name='detail斷言失敗用例')),
                ('case_stat_unexpectedSuccesses', models.IntegerField(null=True, verbose_name='')),
                ('case_time_startat', models.FloatField(verbose_name='開始時間')),
                ('case_duration', models.FloatField(verbose_name='耗時')),
            ],
            options={
                'verbose_name': 'CaseDetail',
                'db_table': 'CaseDetail',
            },
        ),
        migrations.CreateModel(
            name='CaseResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(choices=[('newCar', '新车'), ('usedCar', '中古车')], default='', max_length=10, verbose_name='部门')),
                ('taskid', models.IntegerField(default=0, verbose_name='taskID号')),
                ('success', models.BooleanField(verbose_name='执行结果')),
                ('stat_testsRun', models.IntegerField(verbose_name='執行用例數')),
                ('stat_successes', models.IntegerField(verbose_name='成功用例數')),
                ('stat_failures', models.IntegerField(verbose_name='失敗用例數')),
                ('stat_skipped', models.IntegerField(verbose_name='跳過用例數')),
                ('stat_errors', models.IntegerField(verbose_name='Error用例數')),
                ('stat_expectedFailures', models.IntegerField(null=True, verbose_name='斷言失敗用例')),
                ('stat_unexpectedSuccesses', models.IntegerField(null=True, verbose_name='')),
                ('time_startat', models.FloatField(verbose_name='開始時間')),
                ('duration', models.FloatField(verbose_name='耗時')),
                ('httpRunner_version', models.CharField(max_length=40, verbose_name='HttpRunner版本')),
                ('python_version', models.CharField(max_length=20, verbose_name='python版本')),
                ('platform', models.CharField(max_length=60, verbose_name='系統平臺')),
                ('notes', models.TextField(null=True, verbose_name='備註')),
                ('isnotes', models.BooleanField(default=False, verbose_name='是否备注')),
                ('env', models.CharField(max_length=30, null=True, verbose_name='測試環境')),
                ('reporturl', models.CharField(max_length=80, null=True, verbose_name='报告链接')),
                ('caseDetails', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='autoApi.CaseDetail')),
            ],
            options={
                'verbose_name': '測試執行結果',
                'db_table': 'CaseResult',
            },
        ),
        migrations.CreateModel(
            name='HtmlReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField(null=True, verbose_name='结果详情')),
            ],
            options={
                'verbose_name': 'HtmlReport',
                'db_table': 'HtmlReport',
            },
        ),
        migrations.AddField(
            model_name='caseresult',
            name='reports',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='autoApi.HtmlReport'),
        ),
    ]