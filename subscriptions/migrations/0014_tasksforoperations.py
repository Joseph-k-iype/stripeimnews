# Generated by Django 4.0.4 on 2022-05-19 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscriptions', '0013_remove_ipaddress_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='tasksforoperations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('proof', models.ImageField(blank=True, null=True, upload_to='proofs/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
