# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-27 10:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'cmdb_auth_group_permissions',
            },
        ),
        migrations.CreateModel(
            name='AuthPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('select_host', models.TinyIntegerField()),
                ('update_host', models.TinyIntegerField()),
                ('insert_host', models.TinyIntegerField()),
                ('delete_host', models.TinyIntegerField()),
                ('select_user', models.TinyIntegerField()),
                ('update_user', models.TinyIntegerField()),
                ('delete_user', models.TinyIntegerField()),
                ('insert_user', models.TinyIntegerField()),
            ],
            options={
                'db_table': 'cmdb_auth_permissions',
            },
        ),
        migrations.CreateModel(
            name='HostGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_group_name', models.CharField(max_length=50, unique=True)),
                ('host_group_jd', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'cmdb_host_group',
            },
        ),
        migrations.CreateModel(
            name='HostInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_ip', models.UnsignedIntegerField()),
                ('app_type', models.CharField(max_length=20)),
                ('app_user', models.CharField(max_length=20)),
                ('app_pass', models.CharField(max_length=30)),
                ('app_port', models.SmallIntegerField()),
                ('host_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.HostGroup')),
            ],
            options={
                'db_table': 'cmdb_host_info',
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_group_name', models.CharField(max_length=50, unique=True)),
                ('user_group_jd', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'cmdb_user_group',
            },
        ),
        migrations.CreateModel(
            name='UserHostRelationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lifetime', models.SmallIntegerField()),
                ('expired', models.TinyIntegerField()),
                ('host_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.HostGroup')),
                ('user_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.UserGroup')),
            ],
            options={
                'db_table': 'cmdb_user_host_relationship',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=40, unique=True)),
                ('user_pass', models.CharField(max_length=40)),
                ('user_emails', models.CharField(max_length=100)),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.AuthPermissions')),
            ],
            options={
                'db_table': 'cmdb_user_info',
            },
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_role_name', models.CharField(max_length=50, unique=True)),
                ('user_role_jd', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'cmdb_user_role',
            },
        ),
        migrations.CreateModel(
            name='VerboseName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30, verbose_name="person's first name")),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.UserRole'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.UserGroup'),
        ),
        migrations.AddField(
            model_name='authgrouppermissions',
            name='permission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.AuthPermissions'),
        ),
        migrations.AddField(
            model_name='authgrouppermissions',
            name='user_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmdb.UserGroup'),
        ),
        migrations.AlterUniqueTogether(
            name='userhostrelationship',
            unique_together=set([('user_group', 'host_group')]),
        ),
        migrations.AlterIndexTogether(
            name='hostinfo',
            index_together=set([('host_ip', 'app_type', 'app_port')]),
        ),
    ]