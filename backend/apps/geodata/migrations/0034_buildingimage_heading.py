# Generated by Django 2.1.11 on 2020-01-15 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0033_sector_sector_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingimage',
            name='heading',
            field=models.FloatField(blank=True, help_text='Camera heading.', null=True),
        ),
    ]
