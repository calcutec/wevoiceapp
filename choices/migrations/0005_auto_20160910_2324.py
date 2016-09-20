# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-10 23:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('choices', '0004_auto_20160909_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='choices.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pre_approved', models.BooleanField()),
                ('approved', models.BooleanField()),
                ('rejected', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='selection',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='choices.Status'),
        ),
        migrations.AddField(
            model_name='selection',
            name='talent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='choices.Talent'),
        ),
    ]