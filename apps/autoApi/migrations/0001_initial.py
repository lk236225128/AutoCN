# Generated by Django 2.0 on 2019-03-12 10:12

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
                ('department', models.CharField(choices=[('newCar', '新车'), ('usedCar', '中古车')], default='', max_length=10, verbose_name='部门')),
                ('env', models.CharField(max_length=30, null=True, verbose_name='測試環境')),
                ('case_name', models.CharField(max_length=100, null=True)),
                ('case_success', models.BooleanField(verbose_name='detail执行结果')),
                ('case_stat_testsRun', models.IntegerField(verbose_name='detail執行用例數')),
                ('case_stat_successes', models.IntegerField(verbose_name='detail成功用例數')),
                ('case_stat_failures', models.IntegerField(verbose_name='detail失敗用例數')),
                ('case_stat_skipped', models.IntegerField(verbose_name='detail跳過用例數')),
                ('case_stat_errors', models.IntegerField(verbose_name='detailError用例數')),
                ('case_stat_expectedFailures', models.IntegerField(null=True, verbose_name='detail斷言失敗用例')),
                ('case_stat_unexpectedSuccesses', models.IntegerField(null=True, verbose_name='')),
                ('case_time_startat', models.FloatField(verbose_name='開始時間')),
                ('case_time_startmonth', models.ImageField(null=True, upload_to='', verbose_name='用例执行月份')),
                ('case_time_startyear', models.ImageField(null=True, upload_to='', verbose_name='用例执行年份')),
                ('case_duration', models.FloatField(verbose_name='耗時')),
            ],
            options={
                'verbose_name': '执行详情',
                'verbose_name_plural': '执行详情',
                'db_table': 'CaseDetail',
            },
        ),
        migrations.CreateModel(
            name='CaseResult',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(choices=[('newCar', '新车'), ('usedCar', '中古车')], default='', max_length=10, verbose_name='部门')),
                ('taskid', models.IntegerField(default=0, verbose_name='taskID号')),
                ('runType', models.CharField(default='手动执行', max_length=25, null=True, verbose_name='执行类型')),
                ('success', models.BooleanField(verbose_name='执行结果')),
                ('stat_testsRun', models.IntegerField(verbose_name='執行用例數')),
                ('stat_successes', models.IntegerField(verbose_name='成功用例數')),
                ('stat_failures', models.IntegerField(verbose_name='失敗用例數')),
                ('stat_skipped', models.IntegerField(verbose_name='跳過用例數')),
                ('stat_errors', models.IntegerField(verbose_name='Error用例數')),
                ('passrate', models.FloatField(null=True, verbose_name='通过率')),
                ('stat_expectedFailures', models.IntegerField(null=True, verbose_name='斷言失敗用例')),
                ('stat_unexpectedSuccesses', models.IntegerField(null=True, verbose_name='')),
                ('time_startat', models.FloatField(verbose_name='開始時間')),
                ('duration', models.FloatField(verbose_name='耗時')),
                ('httpRunner_version', models.CharField(max_length=40, verbose_name='HttpRunner版本')),
                ('python_version', models.CharField(max_length=20, verbose_name='python版本')),
                ('platform', models.CharField(default='', max_length=20, verbose_name='平台')),
                ('notesCategory', models.CharField(max_length=100, null=True)),
                ('notes', models.TextField(null=True, verbose_name='備註')),
                ('isnotes', models.BooleanField(default=False, verbose_name='是否备注')),
                ('env', models.CharField(default='testEnv', max_length=30, null=True, verbose_name='測試環境')),
                ('reporturl', models.CharField(max_length=80, null=True, verbose_name='报告链接')),
            ],
            options={
                'verbose_name': '執行結果',
                'verbose_name_plural': '執行結果',
                'db_table': 'CaseResult',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=100)),
                ('departmentName', models.CharField(default='', max_length=100)),
            ],
            options={
                'verbose_name': '部门管理',
                'verbose_name_plural': '部门管理',
                'db_table': 'Department',
            },
        ),
        migrations.CreateModel(
            name='Env',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('env', models.CharField(max_length=100)),
                ('envName', models.CharField(default='', max_length=100)),
            ],
            options={
                'verbose_name': '环境管理',
                'verbose_name_plural': '环境管理',
                'db_table': 'Env',
            },
        ),
        migrations.CreateModel(
            name='HtmlReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField(null=True, verbose_name='结果详情')),
            ],
            options={
                'verbose_name': '测试报告',
                'verbose_name_plural': '测试报告',
                'db_table': 'HtmlReport',
            },
        ),
        migrations.CreateModel(
            name='NotesCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notesCategory', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': '备注类别',
                'verbose_name_plural': '备注类别',
                'db_table': 'notesCategory',
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(default='PC', max_length=20, verbose_name='平台')),
            ],
            options={
                'verbose_name': '平台管理',
                'verbose_name_plural': '平台管理',
                'db_table': 'Platform',
            },
        ),
        migrations.CreateModel(
            name='RunType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('runType', models.CharField(default='手动执行', max_length=25, null=True, verbose_name='执行类型')),
            ],
            options={
                'verbose_name': '执行方式',
                'verbose_name_plural': '执行方式',
                'db_table': 'RunType',
            },
        ),
        migrations.AddField(
            model_name='caseresult',
            name='case_reports',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='autoApi.HtmlReport'),
        ),
        migrations.AddField(
            model_name='casedetail',
            name='caseResult',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='autoApi.CaseResult'),
        ),
    ]
