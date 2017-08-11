# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account_insurer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=45, null=True, blank=True)),
                ('insurer', models.CharField(max_length=45, null=True, blank=True)),
                ('ship_name', models.CharField(max_length=45)),
                ('Clerk', models.CharField(max_length=45, null=True, blank=True)),
                ('Insured_date', models.DateTimeField(null=True, blank=True)),
                ('Expired_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'db_table': 'account_insurer',
            },
        ),
        migrations.CreateModel(
            name='ImportFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'./upload/')),
            ],
            options={
                'ordering': ['file'],
            },
        ),
    ]
