# Generated by Django 4.0.4 on 2022-05-16 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_location_user_parameter_location_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='location_country',
            field=models.CharField(default='0', max_length=120),
        ),
    ]