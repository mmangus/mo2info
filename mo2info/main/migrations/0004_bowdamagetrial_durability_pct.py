# Generated by Django 4.0.3 on 2022-04-09 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_bowdamagepredictor_alter_bowdamagetrial_damage_log"),
    ]

    operations = [
        migrations.AddField(
            model_name="bowdamagetrial",
            name="durability_pct",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
