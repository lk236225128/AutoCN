# Generated by Django 2.0 on 2019-03-14 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoApi', '0005_auto_20190313_0958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caseresult',
            name='taskid',
        ),
        migrations.AddField(
            model_name='caseresult',
            name='cookie',
            field=models.IntegerField(default=0, verbose_name='cookie'),
        ),
        migrations.AddField(
            model_name='caseresult',
            name='runpeople',
            field=models.CharField(default='', max_length=30, verbose_name='执行人'),
        ),
    ]
