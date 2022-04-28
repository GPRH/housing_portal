from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import GeoHash
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from django_pandas.managers import DataFrameManager
from apps.geodata.managers import GPRHMVTManager
from django_extensions.db.fields import AutoSlugField
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.utils.text import slugify
from django.utils.functional import cached_property


class AOI(TimeStampedModel):
    class Meta:
        indexes = [
            models.Index(fields=['country']),
            models.Index(fields=['city']),
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
            models.Index(fields=['sv_key']),
        ]

    country = models.CharField(
        max_length=255,
        help_text=_('Name of the country'),
    )
    city = models.CharField(
        max_length=255,
        help_text=_('Name of the city'),
    )
    name = models.CharField(
        max_length=255,
        help_text=_('Name of the AOI'),
    )
    slug = AutoSlugField(populate_from=['name'], slugify_function=slugify)
    sv_key = models.CharField(
        max_length=255,  blank=True, null=True,
        help_text=_('Mapillary API Start Key'),
    )
    sv_lat = models.FloatField(
        blank=True,  null=True,
    )
    sv_lng = models.FloatField(
        blank=True, null=True,
    )
    geom = models.MultiPolygonField(srid=4326)

    objects = DataFrameManager()

    vector_tiles = GPRHMVTManager()

    def __str__(self):
        return self.name


class Sector(TimeStampedModel):

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    sector_id = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Unique sector id'),
    )

    name = models.CharField(
        max_length=255,
        help_text=_('Name of the Sector'),
    )
    aoi = models.ForeignKey(
        AOI, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='sectors',
    )
    geom = models.MultiPolygonField(srid=4326)

    objects = DataFrameManager()

    vector_tiles = GPRHMVTManager()

    def __str__(self):
        return self.name


class Block(TimeStampedModel):

    class Meta:
        indexes = [
            models.Index(fields=['block_id']),
            models.Index(fields=['k3']),
        ]

    aoi = models.ForeignKey(
        AOI, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='blocks',
    )
    block_id = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Original devseed block id'),
    )
    sector = models.ForeignKey(
        Sector, blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name="blocks",
    )
    k3 = models.FloatField(
        blank=True, null=True,
        help_text=_('COVID-19 Vulnerability Index')
    )
    geom = models.MultiPolygonField(
        srid=4326, help_text=_('Block geometry'),
    )

    objects = DataFrameManager()

    vector_tiles = GPRHMVTManager()

    def __str__(self):
        return self.block_id


class Building(TimeStampedModel):

    class Meta:
        indexes = [
            models.Index(fields=['uid']),
            models.Index(fields=['address']),
            models.Index(fields=['d_material']),
            models.Index(fields=['d_condition']),
            models.Index(fields=['d_avg_height']),
            models.Index(fields=['d_slope']),
            models.Index(fields=['d_volume']),
            models.Index(fields=['d_area']),
            models.Index(fields=['sv_design']),
            models.Index(fields=['sv_complet']),
            models.Index(fields=['sv_materia']),
            models.Index(fields=['sv_use']),
            models.Index(fields=['sv_condit']),
            models.Index(fields=['sv_constru']),
            models.Index(fields=['sv_vintage']),
            models.Index(fields=['sv_securit']),
            models.Index(fields=['sv_window']),
            models.Index(fields=['sv_door']),
            models.Index(fields=['sv_garage']),
            models.Index(fields=['park']),
            models.Index(fields=['infrastruc']),
            models.Index(fields=['hz_earthqu']),
            models.Index(fields=['hz_landslide']),
            models.Index(fields=['hz_flood']),
            models.Index(fields=['hz_wind']),
            models.Index(fields=['hz_tsunami']),
            models.Index(fields=['land_publi']),
            models.Index(fields=['land_servi']),
            models.Index(fields=['count']),
            models.Index(fields=['pt_avg']),
            models.Index(fields=['pt_sum']),
            models.Index(fields=['pt_avg_owed']),
            models.Index(fields=['pt_sum_owed']),
            models.Index(fields=['tot_qualit']),
            models.Index(fields=['soft_story']),
            models.Index(fields=['value']),
            models.Index(fields=['dem_reset']),
            models.Index(fields=['dem_struct']),
            models.Index(fields=['dem_qualit']),
            models.Index(fields=['dem_insur']),
            models.Index(fields=['dem_micro']),
            models.Index(fields=['opp_expansion']),
            models.Index(fields=['cap_payment']),
            models.Index(fields=['k3']),
            GinIndex(
                name='building_extra_attrs_idx', fields=['extra_attrs'],
                opclasses=['jsonb_path_ops']
            ),
            models.Index(fields=['geohash']),
        ]

    uid = models.UUIDField(
        blank=True, null=True,
    )

    # drone attributes
    d_material = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text=_('Condition of roof material'),
    )

    d_condition = models.CharField(
        max_length=255,
        blank=True, null=True,
        help_text=_('Has multilevel roof?'),
    )

    d_avg_height = models.FloatField(
        blank=True, null=True, help_text=_('Average roof height in meters.'),
    )

    d_slope = models.FloatField(
        blank=True, null=True,
        help_text=_('Average slope of terrain in meters'),
    )

    d_volume = models.FloatField(
        blank=True, null=True,
        help_text=_('Volume in cubic meters.'),
    )

    d_area = models.FloatField(
        blank=True, null=True,
        help_text='Area in square meters.',
    )

    # street view attributes
    sv_design = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Is bulding designed?'),
    )

    sv_complet = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Is bulding completed?'),
    )

    sv_materia = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Wall material.'),
    )

    sv_use = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Building use.'),
    )

    sv_securit = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Extra security.'),
    )

    sv_condit = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('General condition.'),
    )

    sv_constru = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Predominant construction type.'),
    )

    sv_vintage = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Vintage of construction.'),
    )

    sv_window = models.IntegerField(
        blank=True, null=True,
        help_text=_('Number of windows.'),
    )

    sv_door = models.IntegerField(
        blank=True, null=True,
        help_text=_('Number of doors.'),
    )

    sv_garage = models.IntegerField(
        blank=True, null=True,
        help_text=_('Number of garages.'),
    )

    # location attributes
    aoi = models.ForeignKey(
        AOI, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='buildings',
    )

    sector = models.ForeignKey(
        Sector, on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='buildings',
    )

    block = models.ForeignKey(
        Block, blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name="buildings",
    )

    address = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('The mailing address.'),
    )

    park = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Within 200m of a park?'),
    )

    infrastruc = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('The sector within the AOI.'),
    )

    # hazard attributes
    hz_earthqu = models.IntegerField(
        blank=True, null=True, default=0,
        help_text=_('Earthquake risk.'),
    )

    hz_landslide = models.IntegerField(
        blank=True, null=True, default=0,
        help_text=_('Landslide risk.'),
    )

    hz_flood = models.IntegerField(
        blank=True, null=True, default=0,
        help_text=_('Flood risk.'),
    )

    hz_wind = models.IntegerField(
        blank=True, null=True, default=0,
        help_text=_('Wind risk.'),
    )

    hz_tsunami = models.IntegerField(
        blank=True, null=True, default=0,
        help_text=_("Tsunami risk.")
    )

    # government / plot attributes
    land_publi = models.IntegerField(
        blank=True, null=True,
        help_text=_('Is public land?'),
    )

    land_servi = models.IntegerField(
        blank=True, null=True,
        help_text=_('Can be serviced?'),
    )

    # tax attributes

    count = models.IntegerField(
        blank=True, null=True, default=0,
        help_text=_(
            """Number of records calculated in
            average property tax per building""",
        ),
    )

    pt_avg = models.IntegerField(
        blank=True, null=True, default=0,
        help_text=_('Average property tax per building'),
    )

    pt_sum = models.IntegerField(
        blank=True, null=True, default=0,
        help_text=_('Sum of property tax per building'),
    )

    pt_avg_owed = models.IntegerField(
        blank=True, null=True, default=0,
        help_text=_('Average property tax owed per building'),
    )

    pt_sum_owed = models.IntegerField(
        blank=True, null=True, default=0,
        help_text=_('Sum of property tax owed per building'),
    )

    # analysis properties

    tot_qualit = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Total quality'),
    )

    soft_story = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Is the building a soft story?'),
    )

    value = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Is the building a soft story?'),
    )

    dem_reset = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Demand for resettlement?'),
    )

    dem_struct = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Demand for strucural improvement only?'),
    )

    dem_qualit = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Demand for quality improvement only?'),
    )

    opp_expansion = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Opportunity for expansion?'),
    )

    cap_payment = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Capacity of payment'),
    )

    dem_insur = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Demand for home insurance premiums?'),
    )

    dem_micro = models.CharField(
        blank=True, null=True, max_length=255,
        help_text=_('Demand for home improvement microloans?'),
    )

    k3 = models.FloatField(
        blank=True, null=True,
        help_text=_("Block level Covid Vulnerabilty Index")
    )

    extra_attrs = JSONField(
        null=True, blank=True,
        help_text=_("Unstructured extra data, eg survey data.")
    )

    # rooftop geometry

    geom = models.MultiPolygonField(
        srid=4326, help_text=_("Building rooftop geometry."),
    )

    geohash = models.CharField(
        blank=True, null=True, max_length=20
    )

    objects = DataFrameManager()

    vector_tiles = GPRHMVTManager()

    def __str__(self):
        return self.uid

    def save(self, *args, **kwargs):
        self._tot_quality()
        self._soft_story()
        # self.value = self._value()

        self._dem_reset()
        self._dem_struct()
        self._dem_qualit()

        self._opp_expansion()
        self._cap_payment()
        self._dem_insur()
        self._dem_micro()
        self._k3()
        self._geohash()

        super(Building, self).save(*args, **kwargs)

    def _tot_quality(self):
        # constants
        VERY_GOOD = 'very good'
        GOOD = 'good'
        FAIR = 'fair'
        POOR = 'poor'
        VERY_POOR = 'very poor'
        GOOD_FAIR = ['good', 'fair']
        DCOND_OTHER_VALUES = ['under construction',
                              'blurred', 'vacant', 'N/A', 'n/a', '']
        SVCOND_OTHER_VALUES = ['N/A', 'n/a', '']

        # very good
        if self.d_condition == GOOD and self.sv_condit == GOOD:
            self.tot_qualit = VERY_GOOD

        # good
        elif (
            self.d_condition == GOOD
            and self.sv_condit in SVCOND_OTHER_VALUES
        ):
            self.tot_qualit = GOOD

        elif (
            self.d_condition in DCOND_OTHER_VALUES and self.sv_condit == GOOD
        ):
            self.tot_qualit = GOOD

        # fair
        elif (
            self.d_condition == FAIR and self.sv_condit == FAIR
        ):
            self.tot_qualit = FAIR

        elif (
            self.d_condition == GOOD and self.sv_condit == FAIR
        ):
            self.tot_qualit = FAIR

        elif (
            self.d_condition == FAIR and self.sv_condit == GOOD
        ):
            self.tot_qualit = FAIR

        elif (
            self.d_condition == FAIR
            and self.sv_condit in SVCOND_OTHER_VALUES
        ):
            self.tot_qualit = FAIR

        elif (
            self.d_condition in DCOND_OTHER_VALUES
            and self.sv_condit == FAIR
        ):
            self.tot_qualit = FAIR

        # poor
        elif (
            self.d_condition == POOR
            and self.sv_condit in GOOD_FAIR + SVCOND_OTHER_VALUES
        ):
            self.tot_qualit = POOR

        elif (
            self.d_condition in GOOD_FAIR + DCOND_OTHER_VALUES
            and self.sv_condit == POOR
        ):
            self.tot_qualit = POOR

        # very poor
        elif (
            self.d_condition == POOR and self.sv_condit == POOR
        ):
            self.tot_qualit = VERY_POOR

        # default
        else:
            self.tot_qualit = None

    def _soft_story(self):
        if (
            self.d_avg_height >= 7.5
            and self.sv_garage >= 1 and self.sv_window >= 2
        ):
            self.soft_story = 'yes'
        else:
            self.soft_story = 'no'

    def _value(self):
        pass  # TODO

    def _dem_reset(self):
        hazzards = (
            self.hz_earthqu == 5 or self.hz_landslide == 5 or
            self.hz_flood == 5 or self.hz_wind == 5 or self.hz_tsunami == 5
        )
        if hazzards and (self.tot_qualit == 'poor'
                         or self.tot_qualit == 'very_poor'):
            self.dem_reset = 'yes'
        else:
            self.dem_reset = 'no'

    def _dem_struct(self):
        hazzards = (
            self.hz_earthqu <= 3 and (
                self.hz_flood <= 4 or self.hz_landslide <= 4 or
                self.hz_wind <= 4)
        )
        constru = (
            self.sv_constru == 'unreinforced_masonry' or
            self.sv_constru == 'reinforced_masonry'
        )
        if (
            hazzards and constru and self.soft_story == 'yes' and
            (self.tot_qualit == 'good' or self.tot_qualit == 'fair')
        ):
            self.dem_struct = 'yes'
        else:
            self.dem_struct = 'no'

    def _dem_qualit(self):
        hazzards = (
            self.hz_flood < 5 and self.hz_landslide < 5 and
            self.hz_earthqu < 5 and self.hz_wind < 5 and
            self.hz_tsunami < 5
        )
        construction = self.sv_constru == 'reinforced_masonry'
        soft_story = self.soft_story == 'yes'
        quality = (self.tot_qualit == 'poor' or self.tot_qualit ==
                   'fair' or self.tot_qualit == 'very_poor')
        if (hazzards and construction and soft_story and quality):
            self.dem_qualit = 'yes'
        else:
            self.dem_qualit = 'no'

    def _opp_expansion(self):
        height = self.d_avg_height < 3
        park = self.park == '1'
        infractructure = self.infrastruc == '1'
        if height and park and infractructure:
            self.opp_expansion = 'yes'
        else:
            self.opp_expansion = 'no'

    def _cap_payment(self):
        self.cap_payment = None  # TODO

    def _dem_insur(self):
        self.dem_insur = None  # TODO

    def _dem_micro(self):
        self.dem_micro = None  # TODO

    def _k3(self):
        if self.block and self.block.k3:
            self.k3 = self.block.k3
        else:
            self.k3 = 3

    def _geohash(self):
        self.geohash = GeoHash(self.geom.centroid, 10)


class Road(TimeStampedModel):

    class Meta:
        indexes = [
            models.Index(fields=['surface']),
            models.Index(fields=['condition']),
            models.Index(fields=['width_m']),
            models.Index(fields=['length_m']),
        ]

    aoi = models.ForeignKey(
        AOI, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='roads',
    )
    surface = models.CharField(
        blank=True, null=True, max_length=255,
    )
    condition = models.CharField(
        blank=True, null=True, max_length=255,
    )
    width_m = models.FloatField(
        blank=True, null=True,
    )
    length_m = models.FloatField(
        blank=True, null=True,
    )
    geom = models.MultiLineStringField(srid=4326)

    objects = DataFrameManager()

    vector_tiles = GPRHMVTManager()


class Plot(TimeStampedModel):

    aoi = models.ForeignKey(
        AOI, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='plots',
    )
    npredial = models.CharField(
        blank=True, null=True, max_length=255,
    )
    estado = models.CharField(
        blank=True, null=True, max_length=255,
    )
    entidad = models.CharField(
        blank=True, null=True, max_length=255,
    )
    objectid_1 = models.IntegerField(
        blank=True, null=True,
    )
    direccion = models.CharField(
        blank=True, null=True, max_length=255,
    )
    destino_ec = models.CharField(
        blank=True, null=True, max_length=255,
    )
    matricula = models.CharField(
        blank=True, null=True, max_length=255,
    )
    juridico = models.CharField(
        blank=True, null=True, max_length=255,
    )
    mejoras = models.BigIntegerField(
        blank=True, null=True,
    )
    geom = models.MultiPolygonField(srid=4326)

    objects = DataFrameManager()

    vector_tiles = GPRHMVTManager()


class Greenspace(TimeStampedModel):
    class Meta:
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['area_m']),
        ]

    aoi = models.ForeignKey(
        AOI, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='greenspaces',
    )

    type = models.CharField(
        blank=True, null=True, max_length=255,
    )

    area_m = models.FloatField(
        blank=True, null=True,
    )

    geom = models.MultiPolygonField(srid=4326)

    objects = DataFrameManager()

    vector_tiles = GPRHMVTManager()


class BuildingImage(TimeStampedModel):
    class Meta:
        indexes = [
            models.Index(fields=['detection_id']),
            models.Index(fields=['image_id']),
            models.Index(fields=['angle']),
            models.Index(fields=['subfolder']),
            models.Index(fields=['frame']),
            models.Index(fields=['cam']),
        ]

    aoi = models.ForeignKey(
        AOI, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='images',
    )

    building = models.ForeignKey(
        Building, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='images',
    )

    detection_id = models.BigIntegerField(
        blank=True, null=True,
    )

    image_id = models.BigIntegerField(
        blank=True, null=True,
    )

    angle = models.FloatField(
        blank=True, null=True,
    )

    subfolder = models.CharField(
        max_length=255, blank=True, null=True,
    )

    frame = models.CharField(
        max_length=254, blank=True, null=True,
    )

    cam = models.CharField(
        max_length=254, blank=True, null=True,
    )

    heading = models.FloatField(
        blank=True, null=True,
        help_text=_('Camera heading.'),
    )

    lat = models.FloatField(
        blank=True, null=True,
        help_text=_('Image latitude.'),
    )

    lon = models.FloatField(
        blank=True, null=True,
        help_text=_('Image longitude.'),
    )

    geom = models.MultiLineStringField(srid=4326)

    objects = DataFrameManager()

    vector_tiles = GPRHMVTManager()

    def __str__(self):
        return "{0}_{1}_Cam{2}.jpg".format(self.subfolder, self.frame, self.cam)


class ConfidenceValue(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['class_str']),
            models.Index(fields=['confidence']),
        ]

    aoi = models.ForeignKey(
        AOI, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='confidence_values',
    )

    building = models.ForeignKey(
        Building, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='confidence_values',
    )

    class_str = models.CharField(
        max_length=255, blank=True, null=True,
    )

    confidence = models.FloatField(
        blank=True, null=True,
        help_text=_('Average confidence value.'),
    )

    bucket = models.IntegerField(
        blank=True, null=True,
        help_text=_('Bucket to which the confidence value is assigned.')
    )

    geom = models.PointField(srid=4326, blank=True, null=True)

    def __str__(self):
        return "{0}: {1}".format(self.class_str, self.confidence)
