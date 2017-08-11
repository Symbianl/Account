# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_management', '0002_account_financing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account_financing',
            old_name='Tel',
            new_name='Borrower_Tel',
        ),
        migrations.RenameField(
            model_name='account_financing',
            old_name='Contact_person',
            new_name='Borrower_user',
        ),
    ]
