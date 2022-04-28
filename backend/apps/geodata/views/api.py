from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Transform, Centroid
from apps.geodata.views.permissions import AOIPermission
from django.conf import settings
from sendfile import sendfile
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from datetime import datetime

from apps.geodata.views.serializers import (
    SimpleAOISerializer, AOISerializer, SectorSerializer, BlockSerializer,
    BuildingSerializer, RoadSerializer, PlotSerializer,
    GreenspaceSerializer, SimpleBuildingSerializer, SectorLabelSerializer
)
from apps.geodata.models import (
    AOI, Sector, Block, Building, Road, Plot, Greenspace,
)
from apps.geodata.views.mixins import (
    AOIQuerysetMixin, RelatedAOIFilterMixin, StatsMixin,
)
from apps.geodata.views.filters import BuildingFilter

IMAGE_DIR = settings.IMAGE_DIR
DRONE_IMAGE_DIR = settings.DRONE_IMAGE_DIR


class SimpleAOIListAPIView(AOIQuerysetMixin, ListAPIView):
    serializer_class = SimpleAOISerializer
    permission_classes = (IsAuthenticated,)


class AOIListAPIView(AOIQuerysetMixin, ListAPIView):
    serializer_class = AOISerializer
    permission_classes = (IsAuthenticated,)
    filter_fields = ['city', 'name']


class SectorListAPIView(RelatedAOIFilterMixin, ListAPIView):
    serializer_class = SectorSerializer
    permission_classes = (IsAuthenticated,)
    filter_fields = ('aoi__name',)

    def get_queryset(self):
        queryset = Sector.objects.all()
        return self._get_filtered_queryset(queryset)


class SectorLabelListAPIView(RelatedAOIFilterMixin, ListAPIView):
    serializer_class = SectorLabelSerializer
    permision_classes = (IsAuthenticated,)
    filter_fields = ('aoi__name',)

    def get_queryset(self):
        queryset = Sector.objects.all()
        return self._get_filtered_queryset(queryset)


class BlockListAPIView(RelatedAOIFilterMixin, ListAPIView):
    serializer_class = BlockSerializer
    permission_classes = (IsAuthenticated,)
    filter_fields = ('aoi__name',)

    def get_queryset(self):
        queryset = Block.objects.all()
        return self._get_filtered_queryset(queryset)


class BuildingListAPIView(RelatedAOIFilterMixin, ListAPIView):
    serializer_class = SimpleBuildingSerializer
    permission_classes = (IsAuthenticated,)
    filterset_class = BuildingFilter

    def get_queryset(self):
        queryset = Building.objects.all()
        return self._get_filtered_queryset(queryset)


class RoadListAPIView(RelatedAOIFilterMixin, ListAPIView):
    serializer_class = RoadSerializer
    permission_classes = (IsAuthenticated,)
    filter_fields = ('aoi__name',)

    def get_queryset(self):
        queryset = Road.objects.all()
        return self._get_filtered_queryset(queryset)


class PlotListAPIView(RelatedAOIFilterMixin, ListAPIView):
    serializer_class = PlotSerializer
    permission_classes = (IsAuthenticated,)
    filter_fields = ('aoi__name',)

    def get_queryset(self):
        queryset = Plot.objects.all()
        return self._get_filtered_queryset(queryset)


class GreenspaceListAPIView(RelatedAOIFilterMixin, ListAPIView):
    serializer_class = GreenspaceSerializer
    permission_classes = (IsAuthenticated,)
    filter_fields = ('aoi__name',)

    def get_queryset(self):
        queryset = Greenspace.objects.all()
        return self._get_filtered_queryset(queryset)


class BuildingRetrieveAPIView(RelatedAOIFilterMixin, RetrieveAPIView):
    serializer_class = BuildingSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Building.objects.all()
        return self._get_filtered_queryset(queryset)


class BuildingImageAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        country = kwargs.get('country')
        aoi = kwargs.get('aoi')
        image = kwargs.get('image')
        path = '{0}{1}/{2}/{3}'.format(
            IMAGE_DIR, country, aoi, image)
        return sendfile(request, path)


class DroneImageryAPIView(APIView):

    permission_classes = (IsAuthenticated, AOIPermission)

    def get(self, request, *args, **kwargs):
        aoi = kwargs.get('aoi')
        z = kwargs.get('z')
        x = kwargs.get('x')
        y = kwargs.get('y')
        path = '{0}{1}/{2}/{3}/{4}.png'.format(
            DRONE_IMAGE_DIR, aoi, z, x, y)
        return sendfile(request, path)


class BlockStatsAPIView(APIView, StatsMixin):

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        data = request.data
        stats = self._get_block_stats(data['blockId'])
        return Response(stats)

    def _get_block_stats(self, blockId):
        blocks = Block.objects.annotate(
            geom_local=Transform('geom', self.get_epsg())
        )
        block = blocks.get(id=blockId)
        sector = block.sector
        building_stats = self._building_stats(obj=block)
        greenspace_stats = self._greenspace_stats(block)
        area = round(block.geom_local.area, 2)
        return {
            'id': blockId,
            'sector': sector.name,
            'buildings': building_stats,
            'greenspace': greenspace_stats,
            'area': area,
        }


class SectorStatsAPIView(APIView, StatsMixin):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        sectorId = request.query_params.get('sectorId')
        stats = self._get_sector_stats(sectorId)
        return Response(stats)

    def _get_sector_stats(self, sectorId):
        sectors = Sector.objects.annotate(
            geom_local=Transform('geom', self.get_epsg()))
        sector = sectors.get(id=sectorId)
        extent = list(sector.geom.extent)
        building_stats = self._building_stats(obj=sector)
        greenspace_stats = self._greenspace_stats(sector)
        k3_stats = self._k3_stats(sector)
        blocks = sector.blocks.count()
        roads = self._road_stats(sector)
        area = round(sector.geom_local.area / 1000000, 2)
        countHeight = sector.buildings.filter(d_avg_height__gt=3.7).count()

        return {
            'id': sectorId,
            'extent': extent,
            'area': area,
            'blocks': blocks,
            'buildings': building_stats,
            'greenspace': greenspace_stats,
            'k3': k3_stats,
            'countHeight': countHeight,
            'roads': roads,
        }


class AOIStatsAPIView(APIView, StatsMixin):

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        aoiId = request.query_params.get('aoiId')
        stats = self._get_aoi_stats(aoiId)
        return Response(stats)

    def _get_aoi_stats(self, aoiId):
        aois = AOI.objects.annotate(
            geom_local=Transform('geom', self.get_epsg())
        )
        aoi = aois.get(id=aoiId)
        extent = list(aoi.geom.extent)
        sectorCount = aoi.sectors.count()
        blockCount = aoi.blocks.count()
        buildings = self._building_stats(obj=aoi)
        greenspace = self._greenspace_stats(aoi)
        k3_stats = self._k3_stats(aoi)
        roads = self._road_stats(aoi)
        area = round(aoi.geom_local.area / 1000000, 2)
        # countHeight = aoi.buildings.filter(d_avg_height__gt=3.7).count()
        return {
            'id': aoiId,
            'extent': extent,
            'name': aoi.name,
            'area': area,
            'sectors': sectorCount,
            'blocks': blockCount,
            'buildings': buildings,
            'greenspace': greenspace,
            'k3': k3_stats,
            'roads': roads,
            # 'countHeight': countHeight,
        }


class AreaStatsAPIView(APIView, StatsMixin):

    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        data = request.data
        geom = GEOSGeometry(str(data['geom']), srid=4326)
        stats = self._get_area_stats(geom=geom)
        return Response(stats)

    def _get_area_stats(self, geom):
        buildings = self._building_stats(geom=geom)
        greenspace = self._greenspace_stats(geom=geom)
        # roads = self._road_stats(aoi)
        building_ids = self._get_building_ids(geom=geom)
        area = round(self._get_area(geom), 2)
        return {
            'area': area,
            'buildings': buildings,
            'building_ids': building_ids,
            'greenspace': greenspace,
            # 'roads': roads,
            # 'countHeight': countHeight,
        }

    def _get_area(self, geom):
        return geom.transform(self.get_epsg(), clone=True).area

    def _get_building_ids(self, geom):
        return Building.objects.annotate(
            centroid=Centroid('geom')).filter(
                centroid__within=geom).values_list(
                    'id', flat=True)


class ExtraAttrFilterAPIView(APIView):
    permission_classes = (IsAuthenticated, AOIPermission)

    def get(self, request, *args, **kwargs):
        attr_key = self.kwargs.get('key')
        attr_value = self.kwargs.get('value')
        building_ids = self._get_building_ids(attr_key, attr_value)
        status_code = status.HTTP_200_OK
        if len(building_ids) == 0:
            status_code = status.HTTP_204_NO_CONTENT
        return Response(building_ids, status=status_code)

    def _get_building_ids(self, key, value):
        kwargs = {
            f'extra_attrs__{key}__value': value
        }
        return Building.objects.filter(**kwargs).values_list(
            'id', flat=True)


class ContactAPIView(APIView):

    allowed_methods = ('POST',)

    def post(self, request, format=None):
        auth_token = request.data.get('auth_token', None)
        if not auth_token or auth_token != settings.CONTACT_FORM_AUTH_TOKEN:
            return Response(status=403)

        email = request.data.get('email', None)
        name = request.data.get('name', None)
        message = request.data.get('message', None)

        # validate post data
        if not email or not self._is_email(email):
            return Response({'email': [_('Invalid email')]}, status=400)
        if not name:
            return Response({'name': [_('Invalid name')]}, status=400)
        if not message:
            return Response({'message': [_('Invalid message')]}, status=400)

        templ = render_to_string(
            'contact/contact_form_submission.txt',
            {
                'email': email, 'name': name,
                'subject': 'GPRH Contact Form Submission',
                'message': message, 'time': datetime.now()
            }
        )
        from_email = settings.CONTACT_FORM_FROM_EMAIL
        recipient_list = settings.CONTACT_FORM_RECIPIENTS
        send_mail('GPRH Contact Form Submission',
                  templ, from_email, recipient_list)
        return Response({'data': 'ok'}, status=200)

    def _is_email(self, email):
        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            return False
        return True
