# Generated by Django 2.1.1 on 2019-10-16 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0015_building_building_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='sv_vintage',
            field=models.CharField(blank=True, help_text='Vintage of construction.', max_length=255, null=True),
        ),
    ]
