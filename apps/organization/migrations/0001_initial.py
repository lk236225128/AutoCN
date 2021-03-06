# Generated by Django 2.0 on 2019-03-12 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
            },
        ),
        migrations.CreateModel(
            name='Env',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('env', models.CharField(max_length=100, verbose_name='执行环境')),
                ('envName', models.CharField(default='', max_length=100)),
            ],
            options={
                'verbose_name': '环境管理',
                'verbose_name_plural': '环境管理',
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(default='PC', max_length=20, verbose_name='运行平台')),
            ],
            options={
                'verbose_name': '平台管理',
                'verbose_name_plural': '平台管理',
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
            },
        ),
    ]
