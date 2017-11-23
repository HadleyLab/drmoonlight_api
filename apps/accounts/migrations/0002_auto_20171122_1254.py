# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-22 12:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resident',
            name='residency_year',
        ),
        migrations.AddField(
            model_name='resident',
            name='residency_years',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Residency years'),
        ),
    ]
