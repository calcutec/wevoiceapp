# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-12 19:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('choices', '0037_delete_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='password',
        ),
    ]