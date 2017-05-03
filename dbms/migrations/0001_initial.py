# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-03 09:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackupedBinlogInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('binlog_name', models.CharField(max_length=50)),
                ('binlog_create_time', models.DateTimeField()),
                ('binlog_size', models.UnsignedSmallIntegerField()),
                ('r_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'dbms_mysql_backuped_binlog_info',
            },
        ),
        migrations.CreateModel(
            name='BackupedInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('backup_name', models.CharField(max_length=100)),
                ('backup_file_path', models.CharField(max_length=100)),
                ('backup_druation', models.UnsignedSmallIntegerField()),
                ('backup_status', models.TinyIntegerField()),
                ('binlog_file_path', models.CharField(max_length=100)),
                ('binlog_index', models.CharField(max_length=100)),
                ('binlog_start', models.CharField(max_length=50)),
                ('binlog_end', models.CharField(max_length=50)),
                ('binlog_backup_status', models.TinyIntegerField(default=0)),
                ('binlog_backup_piece', models.CharField(max_length=50)),
                ('r_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'dbms_mysql_backuped_info',
            },
        ),
        migrations.CreateModel(
            name='BackupPoolInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('pool_name', models.CharField(max_length=50)),
                ('ipaddr', models.IntegerField()),
                ('port', models.UnsignedSmallIntegerField()),
                ('passwd', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'dbms_mysql_backup_pool_source_info',
            },
        ),
        migrations.CreateModel(
            name='InceptionAuditDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sql_sid', models.UnsignedSmallIntegerField()),
                ('status', models.UnsignedSmallIntegerField()),
                ('err_id', models.UnsignedSmallIntegerField()),
                ('stage_status', models.UnsignedSmallIntegerField()),
                ('error_msg', models.CharField(max_length=1000)),
                ('sql_content', models.CharField(max_length=1000)),
                ('aff_row', models.UnsignedSmallIntegerField()),
                ('rollback_id', models.CharField(max_length=50)),
                ('backup_dbname', models.CharField(max_length=100)),
                ('execute_time', models.IntegerField()),
                ('sql_hash', models.CharField(max_length=50)),
                ('r_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'dbms_ince_audit_detail',
            },
        ),
        migrations.CreateModel(
            name='InceptionWorkOrderInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('work_order_id', models.BigIntegerField(unique=True)),
                ('work_user', models.CharField(max_length=50)),
                ('db_host', models.UnsignedIntegerField(default='1000000')),
                ('db_name', models.CharField(default='test_db', max_length=50)),
                ('end_time', models.DateTimeField(default='1980-01-01 01:01:01')),
                ('review_user', models.CharField(max_length=50)),
                ('review_time', models.DateTimeField(default='1980-01-01 01:01:01')),
                ('review_status', models.TinyIntegerField(default=10)),
                ('work_status', models.TinyIntegerField(default=10)),
                ('r_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'dbms_ince_work_order_info',
            },
        ),
        migrations.CreateModel(
            name='InceptionWorkSQL',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sql_content', models.TextField()),
                ('work_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbms.InceptionWorkOrderInfo', to_field='work_order_id')),
            ],
            options={
                'db_table': 'dbms_ince_work_sql_content',
            },
        ),
        migrations.CreateModel(
            name='MysqlBackupSourceInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('generator_room_name', models.CharField(max_length=30)),
                ('ipaddr', models.UnsignedIntegerField()),
                ('port', models.UnsignedSmallIntegerField()),
                ('service_level', models.TinyIntegerField()),
                ('defaults_file', models.CharField(max_length=100)),
                ('back_time', models.TimeField()),
                ('transport_time', models.TimeField(default='1980-01-01 01:01:01')),
                ('is_transport', models.SmallIntegerField(default=0)),
                ('r_time', models.DateTimeField(auto_now_add=True)),
                ('back_pool_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbms.BackupPoolInfo')),
            ],
            options={
                'db_table': 'dbms_mysql_backup_source_info',
            },
        ),
        migrations.AddField(
            model_name='inceptionauditdetail',
            name='work_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbms.InceptionWorkOrderInfo', to_field='work_order_id'),
        ),
        migrations.AddField(
            model_name='backupedinfo',
            name='machine_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbms.MysqlBackupSourceInfo'),
        ),
        migrations.AddField(
            model_name='backupedbinloginfo',
            name='machine_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbms.MysqlBackupSourceInfo'),
        ),
        migrations.AlterUniqueTogether(
            name='mysqlbackupsourceinfo',
            unique_together=set([('generator_room_name', 'ipaddr', 'port')]),
        ),
        migrations.AlterIndexTogether(
            name='backupedinfo',
            index_together=set([('machine_id', 'r_time', 'backup_status')]),
        ),
        migrations.AlterIndexTogether(
            name='backupedbinloginfo',
            index_together=set([('machine_id', 'r_time')]),
        ),
    ]
