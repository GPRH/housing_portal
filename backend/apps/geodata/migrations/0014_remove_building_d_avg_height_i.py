# Generated by Django 2.1.1 on 2019-10-16 11:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0013_rm_building_zone_subzone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='d_avg_height_i',
        ),
    ]
