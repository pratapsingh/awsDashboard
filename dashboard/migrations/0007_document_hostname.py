# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-27 12:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20170224_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='hostname',
            field=models.CharField(default='null', max_length=60),
        ),
    ]
