# Generated by Django 5.1.1 on 2024-10-15 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workers', '0003_alter_worker_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='o2_level',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='temperature',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
