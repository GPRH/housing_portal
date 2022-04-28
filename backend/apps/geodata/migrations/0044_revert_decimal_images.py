# Generated by Django 2.1.11 on 2020-04-09 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0043_switch_to_decimal_building_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingimage',
            name='angle',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='buildingimage',
            name='heading',
            field=models.FloatField(blank=True, help_text='Camera heading.', null=True),
        ),
        migrations.AlterField(
            model_name='buildingimage',
            name='lat',
            field=models.FloatField(blank=True, help_text='Image latitude.', null=True),
        ),
        migrations.AlterField(
            model_name='buildingimage',
            name='lon',
            field=models.FloatField(blank=True, help_text='Image longitude.', null=True),
        ),
    ]
