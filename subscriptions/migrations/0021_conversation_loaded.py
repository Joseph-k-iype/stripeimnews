# Generated by Django 4.0.4 on 2022-05-22 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0020_formforsubmit_prev_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversation',
            name='loaded',
            field=models.BooleanField(default=False),
        ),
    ]
