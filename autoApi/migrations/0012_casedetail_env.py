# Generated by Django 2.0 on 2019-01-08 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoApi', '0011_casedetail_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='casedetail',
            name='env',
            field=models.CharField(max_length=30, null=True, verbose_name='測試環境'),
        ),
    ]
