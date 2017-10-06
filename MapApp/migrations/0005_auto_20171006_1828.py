# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 18:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MapApp', '0004_registerview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mapentity',
            name='entityDescription',
        ),
        migrations.RemoveField(
            model_name='mapentity',
            name='entityName',
        ),
        migrations.RemoveField(
            model_name='mapentity',
            name='lastModDate',
        ),
        migrations.RemoveField(
            model_name='mapentity',
            name='uuid',
        ),
        migrations.AlterField(
            model_name='mapentity',
            name='entityType',
            field=models.CharField(help_text='Insert name here', max_length=60),
        ),
    ]
