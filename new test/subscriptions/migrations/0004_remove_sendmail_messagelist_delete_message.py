# Generated by Django 4.0.4 on 2022-05-16 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_rename_user_sendmail_muser_sendmail_messagelist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sendmail',
            name='messageList',
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]