# Generated by Django 2.0 on 2019-01-11 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoApi', '0013_article_aritcledescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='casedetail',
            name='case_time_startmonth',
            field=models.ImageField(null=True, upload_to='', verbose_name='用例执行月份'),
        ),
        migrations.AddField(
            model_name='casedetail',
            name='case_time_startyear',
            field=models.ImageField(null=True, upload_to='', verbose_name='用例执行年份'),
        ),
    ]