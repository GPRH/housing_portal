# Generated by Django 2.1.1 on 2019-07-26 09:41

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0003_block'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(help_text='Block geometry', srid=4326),
        ),
    ]
