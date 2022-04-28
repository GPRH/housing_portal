import json
from collections import OrderedDict
from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from apps.geodata.models import (
    AOI, Sector, Block, Building, Road, Plot, Greenspace, BuildingImage,
    ConfidenceValue,
)


class ImageSerializer(serializers.ModelSerializer):

    image_name = serializers.SerializerMethodField(read_only=True)
    building_uid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BuildingImage
        fields = (
            'id', 'building_uid', 'image_name', 'angle', 'lat', 'lon',
        )

    def get_image_name(self, obj):
        return '{0}_{1}_Cam{2}.jpg'.format(obj.subfolder, obj.frame, obj.cam)

    def get_building_uid(self, obj):
        if obj.building:
            return obj.building.uid


class ConfidenceValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConfidenceValue
        fields = (
            'class_str', 'confidence', 'bucket'
        )


class SimpleAOISerializer(serializers.ModelSerializer):

    extent = serializers.SerializerMethodField(read_only=True)
    center = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AOI
        fields = ('id', 'country', 'city', 'name', 'slug', 'extent',
                  'center', 'sv_key', 'sv_lat', 'sv_lng')

    def get_extent(self, obj):
        return list(obj.geom.extent)

    def get_center(self, obj):
        center = obj.geom.centroid
        return (center.x, center.y)


class AOISerializer(GeoFeatureModelSerializer):

    class Meta:
        model = AOI
        geo_field = "geom"
        fields = '__all__'


class SectorSerializer(GeoFeatureModelSerializer):

    city = serializers.SerializerMethodField(read_only=True)
    aoi_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Sector
        geo_field = "geom"
        fields = '__all__'

    def get_city(self, obj):
        return obj.aoi.city

    def get_aoi_name(self, obj):
        return obj.aoi.name


class SectorLabelSerializer(GeoFeatureModelSerializer):

    centroid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Sector
        geo_field = 'centroid'
        fields = ('name', 'centroid')

    def get_centroid(self, obj):
        return json.loads(obj.geom.centroid.geojson)


class BlockSerializer(GeoFeatureModelSerializer):

    blk_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Block
        geo_field = 'geom'
        fields = ('id', 'aoi', 'sector', 'blk_id')

    def get_blk_id(self, obj):
        return obj.id


class SimpleBuildingSerializer(GeoFeatureModelSerializer):

    city = serializers.SerializerMethodField(read_only=True)
    aoi_name = serializers.SerializerMethodField(read_only=True)
    sector_name = serializers.SerializerMethodField(read_only=True)
    center = serializers.SerializerMethodField(read_only=True)
    # confidence_values = ConfidenceValueSerializer(many=True)

    class Meta:
        model = Building
        geo_field = "geom"
        fields = (
            'id', 'city', 'aoi_name', 'sector_name', 'address',
            'sector', 'block', 'uid', 'dem_reset', 'soft_story',
            'center',
        )

    def get_city(self, obj):
        return obj.aoi.city

    def get_aoi_name(self, obj):
        return obj.aoi.name

    def get_sector_name(self, obj):
        if obj.sector:
            return obj.sector.name
        else:
            return None

    def get_center(self, obj):
        centroid = obj.geom.centroid
        return [centroid.x, centroid.y]


class BuildingSerializer(GeoFeatureModelSerializer):

    city = serializers.SerializerMethodField(read_only=True)
    aoi_name = serializers.SerializerMethodField(read_only=True)
    sector_name = serializers.SerializerMethodField(read_only=True)
    images = ImageSerializer(many=True)
    confidence_values = ConfidenceValueSerializer(many=True)
    center = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Building
        geo_field = "geom"
        fields = '__all__'

    def get_city(self, obj):
        return obj.aoi.city

    def get_aoi_name(self, obj):
        return obj.aoi.name

    def get_sector_name(self, obj):
        if obj.sector:
            return obj.sector.name
        else:
            return None

    def get_center(self, obj):
        centroid = obj.geom.centroid
        return ["{0:.6f}".format(centroid.x), "{0:.6f}".format(centroid.y)]


class RoadSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Road
        geo_field = 'geom'
        fields = '__all__'


class PlotSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Plot
        geo_field = 'geom'
        fields = '__all__'


class GreenspaceSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Greenspace
        geo_field = 'geom'
        fields = '__all__'
