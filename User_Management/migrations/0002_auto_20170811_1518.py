# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Management', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menger',
            old_name='manager',
            new_name='management',
        ),
    ]
