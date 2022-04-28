# Generated by Django 2.1.11 on 2020-04-27 12:39

from django.db import migrations


def update_aoi_slugs(apps, schema_editor):
    AOI = apps.get_model("geodata", "AOI")
    for aoi in AOI.objects.all():
        aoi.save()


class Migration(migrations.Migration):

    dependencies = [
        ('geodata', '0045_add_aoi_slug_field'),
    ]

    operations = [
        migrations.RunPython(
            update_aoi_slugs, reverse_code=migrations.RunPython.noop,
        )
    ]
