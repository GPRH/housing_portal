from apps.geodata.models import Building


def update_buildings():
    """Save all buldings to apply changes to dynamically calculated values."""
    for building in Building.objects.all().order_by('pk'):
        print('Updating: {0}'.format(building.pk))
        building.save()


def run(*args):
    update_buildings()
