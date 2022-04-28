# Generated by Django 2.1.11 on 2020-04-09 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0041_add_tax_defaults'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='buildingimage',
            name='geodata_bui_confide_f188dd_idx',
        ),
        migrations.RemoveIndex(
            model_name='buildingimage',
            name='geodata_bui_class_s_89d1be_idx',
        ),
        migrations.RemoveField(
            model_name='buildingimage',
            name='class_str',
        ),
        migrations.RemoveField(
            model_name='buildingimage',
            name='confidence',
        ),
    ]
