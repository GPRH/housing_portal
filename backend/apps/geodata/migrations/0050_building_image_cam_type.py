# Generated by Django 2.2.12 on 2020-07-06 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0049_add_building_uuid_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingimage',
            name='cam',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
