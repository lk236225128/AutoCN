# Generated by Django 2.0 on 2019-02-20 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autoApi', '0023_auto_20190220_1126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='platform',
            old_name='platformEn',
            new_name='platform',
        ),
    ]
