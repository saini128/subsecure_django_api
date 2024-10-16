# Generated by Django 5.1.1 on 2024-10-11 20:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.CharField(max_length=4, primary_key=True, serialize=False, unique=True)),
                ('description', models.TextField()),
                ('number_of_workers', models.IntegerField(default=0)),
                ('temperature', models.FloatField()),
                ('o2_level', models.FloatField()),
                ('emergency_bit', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.CharField(max_length=4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workers', to='workers.location')),
            ],
        ),
    ]
