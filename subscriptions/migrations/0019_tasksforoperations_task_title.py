# Generated by Django 4.0.4 on 2022-05-20 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0018_rename_status_tasksforoperations_published_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasksforoperations',
            name='task_title',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
