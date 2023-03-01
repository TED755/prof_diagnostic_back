# Generated by Django 3.0.7 on 2023-03-01 15:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20230301_1517'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activesession',
            old_name='started_at',
            new_name='expired',
        ),
        migrations.RemoveField(
            model_name='activesession',
            name='access_token',
        ),
        migrations.RemoveField(
            model_name='activesession',
            name='refresh_token',
        ),
        migrations.AddField(
            model_name='activesession',
            name='created_at',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
