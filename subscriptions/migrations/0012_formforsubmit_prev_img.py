# Generated by Django 4.0.4 on 2022-05-19 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0011_formforsubmit_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='formforsubmit',
            name='prev_img',
            field=models.ImageField(default=0, upload_to='static/media/'),
            preserve_default=False,
        ),
    ]