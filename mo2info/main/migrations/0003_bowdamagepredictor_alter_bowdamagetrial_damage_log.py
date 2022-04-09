# Generated by Django 4.0.3 on 2022-04-09 06:14

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_bowdamagetrial_damage_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='BowDamagePredictor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formula', models.CharField(max_length=500)),
                ('queryset_filter', models.JSONField(default=dict)),
            ],
        ),
        migrations.AlterField(
            model_name='bowdamagetrial',
            name='damage_log',
            field=models.TextField(help_text='Enter 1 number per line', validators=[django.core.validators.RegexValidator(re.compile('((\\d+)(?:\\s*)){10}'), message='Enter just the 10 numbers, 1 number per line')]),
        ),
    ]
