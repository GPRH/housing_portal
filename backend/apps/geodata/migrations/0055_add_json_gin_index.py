# Generated by Django 2.2.12 on 2020-08-10 09:10

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0054_add_json_field'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='building',
            name='geodata_bui_extra_a_83b16a_idx',
        ),
        migrations.AddIndex(
            model_name='building',
            index=django.contrib.postgres.indexes.GinIndex(fields=['extra_attrs'], name='building_extra_attrs_idx', opclasses=['jsonb_path_ops']),
        ),
    ]
