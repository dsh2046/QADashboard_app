# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-24 21:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_delete_testt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='functional_test_run',
            old_name='total_fail',
            new_name='total_failed',
        ),
        migrations.RenameField(
            model_name='functional_test_run',
            old_name='total_pass',
            new_name='total_passed',
        ),
    ]
