# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 12:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='docfile',
            field=models.FileField(upload_to='documents/clientCertificates/%Y/%m/%d'),
        ),
    ]
