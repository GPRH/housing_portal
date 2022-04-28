# Generated by Django 2.2.12 on 2021-01-28 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0058_add_hz_tsunami_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='hz_earthqu',
            field=models.IntegerField(blank=True, default=0, help_text='Earthquake risk.', null=True),
        ),
        migrations.AlterField(
            model_name='building',
            name='hz_flood',
            field=models.IntegerField(blank=True, default=0, help_text='Flood risk.', null=True),
        ),
        migrations.AlterField(
            model_name='building',
            name='hz_landslide',
            field=models.IntegerField(blank=True, default=0, help_text='Landslide risk.', null=True),
        ),
        migrations.AlterField(
            model_name='building',
            name='hz_tsunami',
            field=models.IntegerField(blank=True, default=0, help_text='Tsunami risk.', null=True),
        ),
        migrations.AlterField(
            model_name='building',
            name='hz_wind',
            field=models.IntegerField(blank=True, default=0, help_text='Wind risk.', null=True),
        ),
    ]
