# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from apps.geodata.imports.layermapping import LayerMapping
from apps.geodata.imports import mappings
from django.contrib.gis.gdal import DataSource
from django.conf import settings
from django.db import connection
from django.db.utils import ProgrammingError


PORTAL_INSTANCE = settings.PORTAL_INSTANCE


def get_model(model_name=None):
    model_type = ContentType.objects.get(
        app_label="geodata", model=model_name,
    )
    model = model_type.model_class()
    return model


def _get_config(aoi):
    return json.loads(
        open('../imports/gpkg/{0}.json'.format(aoi)).read())


def _get_log(layer):
    return "/imports/{0}.log".format(layer)


def delete(aoi=None, layer=None):
    import_config = _get_config(aoi)
    name = import_config['name']
    layers = import_config['layers']
    if layer == 'all':
        for lyr in reversed(layers):
            _delete_layer(name, lyr)
    else:
        for lyr in layers:
            if lyr['name'] == layer:
                _delete_layer(name, lyr)


def import_records(aoi=None, layer=None):
    start = datetime.now()
    print('Starting at: {0}'.format(start))
    import_config = _get_config(aoi)
    layers = import_config['layers']
    name = import_config['name']
    gpkg_path = "/imports/{0}/{1}.gpkg".format(
        PORTAL_INSTANCE.lower(), aoi.lower())
    print('Importing geopackage at: {0}'.format(gpkg_path))
    ds = DataSource(gpkg_path)
    if layer == 'all':
        for lyr in layers:
            _import_layer(name, lyr, ds)
    else:
        for lyr in layers:
            if lyr['name'] == layer:
                _import_layer(name, lyr, ds)
    _cluster_indexes()
    end = datetime.now()
    print('Ending at: {0}'.format(end))
    print('Loading took: {0}'.format(end - start))


def _delete_layer(name, layer):
    model = get_model(model_name=layer['model'])
    if hasattr(model, 'aoi'):
        count = model.objects.filter(aoi__name=name).count()
        model.objects.filter(aoi__name=name).delete()
    else:
        count = model.objects.filter(name=name).count()
        model.objects.filter(name=name).delete()
    print('Deleted {0} {1} records'.format(count, layer['name']))


def _import_layer(name, layer, ds):
    dblayers = layer['db_layers']
    for dblayer in dblayers:
        print(
            'Importing {0} records from {1}'.format(
                layer['name'], dblayer)
        )
        model = get_model(model_name=layer['model'])
        lm = LayerMapping(
            model, ds, mappings.__dict__[
                layer['mapping']],
            layer=layer['name'], transform=True, encoding='utf-8')
        with open(_get_log(layer['name']), 'w') as f:
            lm.save(verbose=True, stream=f, progress=500)
    if hasattr(model, 'aoi'):
        count = model.objects.filter(aoi__name=name).count()
    else:
        count = model.objects.filter(name=name).count()
    print('Imported {0} {1} records.'.format(count, layer['name']))


def _cluster_indexes():
    with connection.cursor() as cursor:
        cursor.execute("CLUSTER geodata_aoi USING geodata_aoi_geom_id")
        cursor.execute(
            "CLUSTER geodata_sector USING geodata_sector_geom_id"
        )
        try:
            cursor.execute(
                "CREATE INDEX geodata_building_idx_geohash ON geodata_building (ST_GeoHash(geom))")
        except ProgrammingError:
            pass
        cursor.execute(
            "CLUSTER geodata_building USING geodata_building_idx_geohash")
        cursor.execute(
            "CLUSTER geodata_greenspace USING geodata_greenspace_geom_id")
        cursor.execute(
            "CLUSTER geodata_road USING geodata_road_geom_id")


def run(*args):
    if (len(args) > 0):
        if args[0] == 'cluster':
            _cluster_indexes()
            return
    if len(args) != 3:
        print("Args: 'import|overwrite|delete <aoi> all|layer'")
        return
    if args[0] == 'delete':
        delete(aoi=args[1], layer=args[2])
        return
    if args[0] == 'overwrite':
        delete(aoi=args[1], layer=args[2])
        import_records(aoi=args[1], layer=args[2])
        return
    if args[0] == 'import':
        import_records(aoi=args[1], layer=args[2])
    if args[0] == 'cluster':
        _cluster_indexes()
