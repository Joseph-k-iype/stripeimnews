# Generated by Django 4.0.4 on 2022-05-19 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0010_remove_conversation_chat_conversation_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='formforsubmit',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]