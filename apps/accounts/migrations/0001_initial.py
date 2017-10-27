# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 10:05
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_fsm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
                'swappable': 'AUTH_USER_MODEL',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ResidencyProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Residency program',
                'verbose_name_plural': 'Residency programs',
            },
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Speciality',
                'verbose_name_plural': 'Specialities',
            },
        ),
        migrations.CreateModel(
            name='AccountManager',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Account manager',
                'verbose_name_plural': 'Account manager',
            },
            bases=('accounts.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('earliest_availability_for_shift', models.TextField(blank=True, verbose_name='Earliest availability for a shift')),
                ('preferences_for_work_location', models.TextField(blank=True, verbose_name='Preferences for a work location')),
                ('state_license', models.BooleanField(default=False, verbose_name='Has state licence')),
                ('federal_dea_active', models.BooleanField(default=False, verbose_name='Is federal dea active')),
                ('bls_acls_pals', models.NullBooleanField(default=None, verbose_name='Has BLC/ACLS/PALS')),
                ('active_permanent_residence_card_or_visa', models.NullBooleanField(default=None, verbose_name='Has active permanent residence card or visa')),
                ('active_current_driver_license_or_passport', models.BooleanField(default=False, verbose_name='Has active current driver license or passport')),
                ('active_npi_number', models.BooleanField(default=False, verbose_name='Has active npi number')),
                ('ecfmg', models.NullBooleanField(default=None, verbose_name='ECFMG')),
                ('active_board_certificates', models.NullBooleanField(default=None, verbose_name='Has active board certificates')),
                ('notification_new_shifts', models.BooleanField(default=True, verbose_name='Notify about new shifts')),
                ('notification_application_status_changing', models.BooleanField(default=True, verbose_name='Notify about an application status changing')),
                ('notification_new_messages', models.BooleanField(default=True, verbose_name='Notify about new messages')),
                ('residency_year', models.PositiveIntegerField(blank=True, null=True, verbose_name='Residency year')),
                ('state', django_fsm.FSMIntegerField(default=1, verbose_name='State')),
                ('residency_program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.ResidencyProgram', verbose_name='Residency program')),
                ('specialities', models.ManyToManyField(blank=True, to='accounts.Speciality', verbose_name='Specialities')),
            ],
            options={
                'verbose_name': 'Resident',
                'verbose_name_plural': 'Residents',
            },
            bases=('accounts.user', models.Model),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Scheduler',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('facility_name', models.CharField(max_length=255, verbose_name='Facility name')),
                ('department_name', models.CharField(max_length=255, verbose_name='Department name')),
                ('state', django_fsm.FSMIntegerField(default=1, verbose_name='State')),
            ],
            options={
                'verbose_name': 'Scheduler',
                'verbose_name_plural': 'Schedulers',
            },
            bases=('accounts.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
