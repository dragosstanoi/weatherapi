# Generated by Django 4.0.4 on 2022-05-16 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_location_location_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='unitsofmeasurment',
            field=models.CharField(default='metric', max_length=120),
        ),
    ]