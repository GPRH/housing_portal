# Generated by Django 2.1.11 on 2020-04-09 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0042_update_image_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildingimage',
            name='angle',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='buildingimage',
            name='heading',
            field=models.DecimalField(blank=True, decimal_places=6, help_text='Camera heading.', max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='buildingimage',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=6, help_text='Image latitude.', max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='buildingimage',
            name='lon',
            field=models.DecimalField(blank=True, decimal_places=6, help_text='Image longitude.', max_digits=9, null=True),
        ),
    ]
