# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 09:49
from __future__ import unicode_literals

import apps.main.models.mixins.timestamp
import contrib.easymoney
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', django_fsm.FSMIntegerField(default=1, verbose_name='State')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='accounts.Resident', verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Application',
                'verbose_name_plural': 'Applications',
            },
            bases=(apps.main.models.mixins.timestamp.TimestampModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Message')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='shifts.Application', verbose_name='Application')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
            bases=(apps.main.models.mixins.timestamp.TimestampModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateTimeField(verbose_name='Date start')),
                ('date_end', models.DateTimeField(verbose_name='Date end')),
                ('residency_years_required', models.PositiveIntegerField(default=0, verbose_name='Residency years required')),
                ('payment_amount', contrib.easymoney.MoneyField(max_digits=12, verbose_name='Payment amount')),
                ('payment_per_hour', models.BooleanField(verbose_name='Payment per hour')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shifts', to='accounts.Scheduler', verbose_name='Owner')),
                ('residency_program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.ResidencyProgram', verbose_name='Residency program')),
                ('speciality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Speciality', verbose_name='Speciality')),
            ],
            options={
                'verbose_name': 'Shift',
                'verbose_name_plural': 'Shifts',
            },
            bases=(apps.main.models.mixins.timestamp.TimestampModelMixin, models.Model),
        ),
        migrations.AddField(
            model_name='application',
            name='shift',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='shifts.Shift', verbose_name='Shift'),
        ),
    ]
