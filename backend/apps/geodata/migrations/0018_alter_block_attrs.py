# Generated by Django 2.1.1 on 2019-10-17 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0017_add_building_tax_attrs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='area_m2',
        ),
        migrations.RemoveField(
            model_name='block',
            name='barrio',
        ),
        migrations.RemoveField(
            model_name='block',
            name='coddane',
        ),
        migrations.RemoveField(
            model_name='block',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='block',
            name='loc',
        ),
        migrations.RemoveField(
            model_name='block',
            name='long_mt',
        ),
        migrations.RemoveField(
            model_name='block',
            name='manzana',
        ),
        migrations.RemoveField(
            model_name='block',
            name='sector_name',
        ),
        migrations.RemoveField(
            model_name='block',
            name='ucg',
        ),
        migrations.AddField(
            model_name='block',
            name='block_id',
            field=models.IntegerField(blank=True, help_text='Original devseed block id', null=True),
        ),
    ]
