# Generated by Django 2.2.12 on 2021-01-27 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0056_building_hz_tsunami'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='building',
            name='geodata_bui_dem_bot_f5c543_idx',
        ),
        migrations.RemoveIndex(
            model_name='building',
            name='geodata_bui_sv_disa_2f4d96_idx',
        ),
        migrations.RemoveField(
            model_name='building',
            name='d_multilevel',
        ),
        migrations.RemoveField(
            model_name='building',
            name='dem_both',
        ),
        migrations.RemoveField(
            model_name='building',
            name='sv_disaster',
        ),
    ]