# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-16 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choices', '0003_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='upload',
            name='audio_files',
            field=models.FileField(upload_to='/bulk_upload'),
        ),
    ]
