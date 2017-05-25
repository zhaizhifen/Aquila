# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-24 15:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbms', '0003_auto_20170524_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkOrderTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_ip', models.CharField(max_length=45, unique=True)),
                ('app_user', models.CharField(max_length=20)),
                ('app_pass', models.CharField(max_length=30)),
                ('app_port', models.SmallIntegerField()),
                ('wid', models.BigIntegerField(unique=True)),
            ],
        ),
    ]