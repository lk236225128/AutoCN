# Generated by Django 2.0 on 2019-02-14 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoApi', '0020_auto_20190213_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='caseresult',
            name='platform',
            field=models.CharField(default='', max_length=20, verbose_name='平台'),
        ),
        migrations.AlterField(
            model_name='platform',
            name='platform',
            field=models.CharField(choices=[('iOS', 'iOS'), ('Android', 'Android'), ('H5', '触屏'), ('PC', 'PC')], default='PC', max_length=20, verbose_name='平台'),
        ),
    ]
