# Generated by Django 2.0 on 2019-03-12 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autoApi', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.DeleteModel(
            name='Env',
        ),
        migrations.DeleteModel(
            name='Platform',
        ),
        migrations.DeleteModel(
            name='RunType',
        ),
    ]
