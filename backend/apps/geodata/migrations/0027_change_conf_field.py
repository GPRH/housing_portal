# Generated by Django 2.1.11 on 2019-11-13 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0026_add_fields_building_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingimage',
            name='confidence',
            field=models.FloatField(blank=True, null=True),
        ),
    ]