# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-02 18:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MapApp', '0002_auto_20160420_2128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mapentity',
            name='endDate',
        ),
        migrations.RemoveField(
            model_name='mapentity',
            name='startDate',
        ),
        migrations.AlterField(
            model_name='mapentity',
            name='entityDescription',
            field=models.TextField(help_text='Very awesome party at my place', max_length=300),
        ),
        migrations.AlterField(
            model_name='mapentity',
            name='entityName',
            field=models.CharField(help_text='Insert name here', max_length=60),
        ),
        migrations.AlterField(
            model_name='mapentity',
            name='entityType',
            field=models.ForeignKey(help_text='What type of event is it?', on_delete=django.db.models.deletion.CASCADE, to='MapApp.EventType'),
        ),
    ]
