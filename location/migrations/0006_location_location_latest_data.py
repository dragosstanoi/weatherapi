# Generated by Django 4.0.4 on 2022-05-17 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0005_alter_location_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='location_latest_data',
            field=models.TextField(blank=True, null=True),
        ),
    ]
