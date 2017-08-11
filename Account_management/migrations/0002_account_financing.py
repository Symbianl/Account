# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account_financing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=45, null=True, blank=True)),
                ('Blank', models.CharField(max_length=45, null=True, blank=True)),
                ('ship_name', models.CharField(max_length=45)),
                ('Clerk', models.CharField(max_length=45, null=True, blank=True)),
                ('sum', models.CharField(max_length=45, null=True, blank=True)),
                ('Contact_person', models.CharField(max_length=45, null=True, blank=True)),
                ('Tel', models.BigIntegerField(null=True, blank=True)),
                ('Expired_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'account_financing',
            },
        ),
    ]
