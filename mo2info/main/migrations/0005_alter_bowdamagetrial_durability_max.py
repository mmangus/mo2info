# Generated by Django 4.0.3 on 2022-04-11 03:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_bowdamagetrial_durability_pct"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bowdamagetrial",
            name="durability_max",
            field=models.FloatField(
                help_text="Maximum durability of the bow",
                validators=[django.core.validators.MinValueValidator(0.1)],
            ),
        ),
    ]
