"""Dataset download API views."""

import os
import pathlib
import shutil
import geopandas as gpd
import zipfile
import tempfile
from shapely import wkt
from collections import OrderedDict
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.db.models import (
    Count, Sum, Q, ExpressionWrapper, FloatField,
    When, Case
)
from rest_framework.exceptions import ValidationError
from django.db.models.fields.related import ForeignKey
from django.contrib.gis.db.models.functions import Area, Transform
from apps.geodata.models import (
    AOI, Sector, Block, Building, Road, Greenspace,
)
from django.utils.text import slugify


FORMATS = ['geojson', 'shp', 'csv', 'gpkg']

DATASETS = {
    'sectors': Sector, 'blocks': Block, 'buildings': Building,
    'roads':  Road, 'greenspace': Greenspace,
}

SCHEMAS = {
    'sectors': {
        'geometry': 'MultiPolygon',
        'properties': OrderedDict(
            [('id', 'int'), ('sector_id', 'str'), ('name', 'str'),
             ('building_count', 'int'), ('very_poor_quality', 'int'),
             ('poor_quality', 'int'), ('fair_quality', 'int'),
             ('good_quality', 'int'), ('very_good_quality', 'int'),
             ('residential', 'int'), ('commercial', 'int'), ('mixed', 'int'),
             ('critical_infrastructure', 'int'),
             ('resettlement', 'int'), ('softstory', 'int'),
             ('avg_tax', 'float:10.2'), ('avg_tax_owed', 'float:10.2'),
             ('area_km', 'float:10.2')])}
}

EXPORT_DIR = settings.EXPORTS_DIR
METADATA_DIR = str(settings.EXPORTS_METADATA_DIR)
DOMAIN = settings.DOMAIN
COUNTRY = settings.PORTAL_INSTANCE.lower()
EPSG = settings.LOCAL_EPSG


class Export(object):

    def __init__(self, aoi, dataset, format):
        self._validate_data(aoi, dataset, format)
        self.aoi = aoi
        self.dataset = dataset
        self.format = format
        self.qs = None

    def export_dataset(self):
        qs = self._filter_data()
        if qs.count() == 0:
            return None
        self.qs = qs
        if self.dataset == 'sectors':
            self._aggregate_sector_data()
        zf = self._package_download()
        return {'zipfile': zf}

    def _validate_data(self, aoi, dataset, format):
        if not aoi or not dataset or not format:
            raise ValidationError(_('Invalid export arguments.'))
        if dataset not in DATASETS.keys():
            raise ValidationError(_('Invalid dataset.'))
        if(format is None or format == '' or format not in FORMATS):
            raise ValidationError(_('Invalid format.'))
        if not AOI.objects.filter(name=aoi).exists():
            raise ValidationError(_('Invalid Area of Interest'))

    def _filter_data(self):
        model = DATASETS.get(self.dataset)
        if hasattr(model, 'aoi'):
            return model.objects.filter(aoi__name=self.aoi)
        else:
            return model.objects.filter(name=self.aoi)

    def _package_download(self):
        gdf = self._get_geodataframe()
        aoiname = slugify(self.aoi)
        export_dir = '{0}{1}/{2}'.format(
            EXPORT_DIR, COUNTRY, aoiname
        )
        filename = '{0}-{1}'.format(aoiname, self.dataset)
        if not os.path.exists(export_dir):
            os.makedirs(export_dir, exist_ok=True)
        with tempfile.TemporaryDirectory() as tempdir:
            if self.dataset in ['sectors', 'buildings']:
                metadata_file = "{0}/{1}".format(
                    METADATA_DIR, 'housing_passport_metadata.pdf')
                shutil.copy(metadata_file, tempdir)
            if self.dataset == 'buildings' and aoiname == 'chacarita':
                metadata_file = "{0}/{1}".format(
                    METADATA_DIR, 'housing_passport_survey_metadata.pdf')
                shutil.copy(metadata_file, tempdir)
            if (self.format == 'shp'):
                fp = '{0}/{1}{2}'.format(tempdir, filename, '.shp')
                schema = SCHEMAS.get(self.dataset, None)
                gdf.to_file(
                    fp, encoding='utf-8', schema=schema,
                    driver='ESRI Shapefile', layer=self.dataset
                )
                zf = self._makezip(tempdir, filename)
            if (self.format == 'gpkg'):
                fp = '{0}/{1}{2}'.format(tempdir, filename, '.gpkg')
                gdf.to_file(
                    fp, encoding='utf-8',
                    driver='GPKG', layer=self.dataset
                )
                zf = self._makezip(tempdir, filename)
            if (self.format == 'geojson'):
                fp = '{0}/{1}{2}'.format(tempdir, filename, '.geojson')
                gdf.to_file(fp, encoding='utf-8',
                            driver='GeoJSON')
                zf = self._makezip(tempdir, filename)
            if (self.format == 'csv'):
                fp = '{0}/{1}{2}'.format(tempdir, filename, '.csv')
                gdf.to_file(
                    fp, driver='CSV', encoding='utf-8',
                    **{'GEOMETRY_NAME': 'geom',
                       'GEOMETRY': 'AS_WKT',
                       'CREATE_CSVT': 'Yes'}
                )
                zf = self._makezip(tempdir, filename)
            export_file = os.path.join(export_dir, zf)
            tmpfile = os.path.join(tempdir, zf)
            shutil.copy(tmpfile, export_file)
            return export_file

    def _makezip(self, tempdir, filename):
        files = []
        curdir = os.getcwd()
        os.chdir(tempdir)
        path = pathlib.Path('.')
        for file in path.glob('**/*.*'):
            files.append(file)
        zf = '{0}-{1}.zip'.format(filename, self.format)
        with zipfile.ZipFile(zf, mode='w',
                             compression=zipfile.ZIP_DEFLATED) as z:
            for f in files:
                z.write(f)
        assert os.path.exists(zf), 'Error creating export.'
        os.chdir(curdir)
        return zf

    def _get_geodataframe(self):
        fieldnames = self._fieldnames(self.qs.model)
        df = self.qs.to_dataframe(verbose=True, fieldnames=fieldnames)
        df = df.drop(columns=['created', 'modified'])
        df['geom'] = df['geom'].apply(self._parse_geom)
        if self.dataset == 'buildings':
            df['d_material'] = df['d_material'].apply(self._parse_d_material)
        if self.dataset == 'sectors':
            df['area_km'] = df['area_km'].apply(self._get_area_km)
        df = df.round(decimals={'avg_tax': 2, 'avg_tax_owed': 2})
        gdf = gpd.GeoDataFrame(df, geometry='geom', crs='EPSG:4326')
        return gdf

    def _parse_geom(self, geom):
        return wkt.loads(geom.wkt)

    def _get_area_km(self, area_km):
        sq_km = round(area_km.sq_km, 2)
        return float(sq_km)

    def _parse_d_material(self, d_material):
        if d_material == 'tile-metal' or d_material == 'tile-clay':
            return d_material.split('-')[0]
        else:
            return d_material

    def _fieldnames(self, model):
        fieldnames = []
        fields = model._meta.fields
        for field in fields:
            if isinstance(field, ForeignKey) or field.name == 'uid':
                continue
            else:
                fieldnames.append(field.name)
        if model._meta.model_name.lower() == 'sector':
            fieldnames += ['building_count', 'very_poor_quality',
                           'poor_quality', 'fair_quality',
                           'good_quality', 'very_good_quality',
                           'residential', 'commercial', 'mixed',
                           'critical_infrastructure', 'resettlement',
                           'softstory', 'avg_tax', 'avg_tax_owed', 'area_km']
        return tuple(fieldnames)

    def _aggregate_sector_data(self):
        self.qs = self.qs.annotate(
            building_count=Count('buildings'),
            very_poor_quality=Count('buildings', filter=Q(
                buildings__tot_qualit='very poor')),
            poor_quality=Count('buildings', filter=Q(
                buildings__tot_qualit='poor')),
            fair_quality=Count('buildings', filter=Q(
                buildings__tot_qualit='fair')),
            good_quality=Count('buildings', filter=Q(
                buildings__tot_qualit='good')),
            very_good_quality=Count('buildings', filter=Q(
                buildings__tot_qualit='very good')),
            residential=Count('buildings', filter=Q(
                buildings__sv_use='residential')),
            commercial=Count('buildings', filter=Q(
                buildings__sv_use='non_residential')),
            mixed=Count('buildings', filter=Q(
                buildings__sv_use='mixed')),
            critical_infrastructure=Count('buildings', filter=Q(
                buildings__sv_use='critical_infrastructure'
            )),
            resettlement=Count('buildings', filter=Q(
                buildings__dem_reset='YES')),
            softstory=Count('buildings', filter=Q(
                buildings__soft_story='YES')),
            total_tax_records=Sum('buildings__count'),
            avg_tax=Case(
                When(total_tax_records__gt=0,
                     then=ExpressionWrapper(
                         Sum('buildings__pt_avg') * Decimal('1.0') /
                         Sum('buildings__count'),
                         output_field=FloatField()),
                     ),
                default=0.0,
                output_field=FloatField()
            ),
            avg_tax_owed=Case(
                When(total_tax_records__gt=0,
                     then=ExpressionWrapper(
                         Sum('buildings__pt_avg_owed') * Decimal('1.0') /
                         Sum('buildings__count'),
                         output_field=FloatField()),
                     ),
                default=0.0,
                output_field=FloatField()
            ),
            area_km=Area(Transform('geom', EPSG))
        )
