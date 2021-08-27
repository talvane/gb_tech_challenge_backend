# Generated by Django 3.2.6 on 2021-08-27 18:05

import apps.sales.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_auto_20210827_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='value',
            field=models.FloatField(validators=[apps.sales.models.validate_value], verbose_name='Product Value'),
        ),
    ]