# Generated by Django 2.0 on 2019-03-18 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoApi', '0006_auto_20190314_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casedetail',
            name='case_time_startmonth',
            field=models.IntegerField(null=True, verbose_name='用例执行月份'),
        ),
        migrations.AlterField(
            model_name='casedetail',
            name='case_time_startyear',
            field=models.IntegerField(null=True, verbose_name='用例执行年份'),
        ),
    ]