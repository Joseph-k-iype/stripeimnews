# Generated by Django 4.0.4 on 2022-10-01 06:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0037_task_description_alter_messages_timesent_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='description',
        ),
        migrations.RemoveField(
            model_name='task',
            name='task_status',
        ),
        migrations.AddField(
            model_name='task',
            name='taskstatus',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='messages',
            name='timeSent',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 1, 6, 45, 57, 593700)),
        ),
    ]