# Generated by Django 3.0.7 on 2023-02-26 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('access_token', models.CharField(max_length=500)),
                ('refresh_token', models.CharField(max_length=500)),
                ('start_date', models.DateField()),
                ('start_time', models.TimeField()),
            ],
        ),
    ]
