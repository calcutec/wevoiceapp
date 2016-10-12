# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-05 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choices', '0033_remove_client_last_modified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='talent',
            name='allclients',
        ),
        migrations.AlterField(
            model_name='talent',
            name='age_range',
            field=models.CharField(blank=True, choices=[('1-15', '1-15'), ('16-25', '16-25'), ('26-45', '26-45'), ('46-75', '46-75'), ('75 +', '75 +')], default=3, max_length=32, null=True),
        ),
    ]