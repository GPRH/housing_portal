# Generated by Django 2.1.11 on 2020-01-17 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0035_add_image_lat_lon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='sv_vintage',
            field=models.CharField(blank=True, help_text='Vintage of construction.', max_length=255, null=True),
        ),
    ]
