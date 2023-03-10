# Generated by Django 3.0.7 on 2023-03-05 11:10

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20230301_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnostic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('diagnostic_type', models.TextField(default='standard', max_length=15)),
                ('answers', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True), size=45)),
            ],
        ),
    ]
