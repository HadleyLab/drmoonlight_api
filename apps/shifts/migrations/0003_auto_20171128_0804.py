# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-28 08:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shifts', '0002_auto_20171122_1254'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='message',
            new_name='text',
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(verbose_name='Text'),
        ),
    ]
