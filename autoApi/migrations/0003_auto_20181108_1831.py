# Generated by Django 2.1.3 on 2018-11-08 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoApi', '0002_auto_20181108_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caseresult',
            name='start_datetime',
            field=models.CharField(max_length=20, verbose_name='開始時間'),
        ),
    ]
