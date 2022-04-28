aoi = {
    'country': 'country',
    'city': 'city',
    'name': 'name',
    'sv_key': 'sv_key',
    'sv_lat': 'lat',
    'sv_lng': 'lng',
    'geom': 'MULTIPOLYGON',
}

sectors = {
    'sector_id': 'sector_id',
    'name': 'sector',
    'aoi': {'name': 'aoi'},
    'geom': 'MULTIPOLYGON',
}

blocks = {
    'aoi': {'name': 'aoi'},
    'sector': {'name': 'sector'},
    'block_id': 'block_id',
    'k3': 'k3',
    'geom': 'MULTIPOLYGON',
}

roads = {
    'aoi': {'name': 'aoi'},
    'surface': 'surface',
    'condition': 'condition',
    'width_m': 'width_m',
    'length_m': 'length_m',
    'geom': 'MULTILINESTRING',
}

buildings = {
    'uid': 'uid',
    'block': {'block_id': 'block_id'},
    'd_material': 'd_material',
    'd_condition': 'd_conditio',
    'd_avg_height': 'd_avg_hgt',
    'd_slope': 'd_slope',
    'd_volume': 'd_volume',
    'd_area': 'd_area',
    'sv_design': 'sv_design',
    'sv_complet': 'sv_complet',
    'sv_materia': 'sv_materia',
    'sv_use': 'sv_use',
    'sv_securit': 'sv_securit',
    'sv_condit': 'sv_condit',
    'sv_vintage': 'sv_vintage',
    'sv_constru': 'sv_constru',
    'sv_window': 'sv_window',
    'sv_door': 'sv_door',
    'sv_garage': 'sv_garage',
    'aoi': {'name': 'aoi'},
    'sector': {'sector_id': 'sector_id'},
    'address': 'address',
    'park': 'park',
    'infrastruc': 'infrastruc',
    'hz_earthqu': 'hz_earthqu',
    'hz_flood': 'hz_flood',
    'hz_landslide': 'hz_landsli',
    'hz_wind': 'hz_wind',
    'hz_tsunami': 'hz_tsunami',
    'land_publi': 'land_publi',
    'land_servi': 'land_servi',
    'count': 'count',
    'pt_avg': 'pt_avg',
    'pt_sum': 'pt_sum',
    'pt_avg_owed': 'pt_avg_o',
    'pt_sum_owed': 'pt_sum_o',
    'value': 'value',
    'extra_attrs': 'extra_attrs',
    'geom': 'MULTIPOLYGON',
}

plots = {
    'aoi': {'name': 'aoi'},
    'npredial': 'npredial',
    'estado': 'estado',
    'entidad': 'entidad',
    'objectid_1': 'OBJECTID_1',
    'direccion': 'DIRECCION',
    'destino_ec': 'DESTINO_EC',
    'matricula': 'MATRICULA',
    'juridico': 'JURIDICO',
    'mejoras': 'MEJORAS',
    'geom': 'MULTIPOLYGON',
}


greenspaces = {
    'aoi': {'name': 'aoi'},
    'type': 'type',
    'area_m': 'area_m',
    'geom': 'MULTIPOLYGON',
}

images = {
    'aoi': {'name': 'aoi'},
    'building': {'uid': 'uid'},
    'detection_id': 'detection_id',
    'image_id': 'image_id',
    'angle': 'angle',
    'subfolder': 'subfolder',
    'frame': 'frame',
    'cam': 'cam',
    'heading': 'heading',
    'lat': 'lat',
    'lon': 'lon',
    'geom': 'LINESTRING',
}

building_confidence = {
    'aoi': {'name': 'aoi'},
    'building': {'uid': 'uid'},
    'class_str': 'class_str',
    'confidence': 'confidence',
    'bucket': 'bucket',
    'geom': 'POINT',
}
