from apps.geodata.models import (
    AOI, Sector, Block, Building, Road, Plot, Greenspace,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_mvt.views import BaseMVTView
from apps.geodata.views.permissions import AOIPermission
from rest_framework.serializers import ValidationError
from rest_framework_gis.filters import TMSTileFilter
from rest_framework.response import Response


class BaseGeodataMVTView(BaseMVTView):
    permission_classes = (IsAuthenticated, AOIPermission)


class ClusteredGeodataMVTView(BaseGeodataMVTView):

    def get(self, request, *args, **kwargs):
        """
        Args:
            request (:py:class:`rest_framework.request.Request`): Standard DRF request object
        Returns:
            :py:class:`rest_framework.response.Response`:  Standard DRF response object
        """
        tile_param = 'tile'
        params = request.GET.dict()
        if params.pop("tile", None) is not None:
            try:
                limit, offset = self._validate_paginate(
                    params.pop("limit", None), params.pop("offset", None)
                )
            except ValidationError:
                limit, offset = None, None
            bbox = TMSTileFilter().get_filter_bbox(request)
            tile_string = request.query_params.get(tile_param, None)
            z, x, y = (int(n) for n in tile_string.split('/'))
            try:
                mvt = self.model.clustered_vector_tiles.intersect(
                    bbox=bbox, zoom=z, limit=limit,
                    offset=offset, filters=params
                )
                status = 200 if mvt else 204
            except ValidationError:
                mvt = b""
                status = 400
        else:
            mvt = b""
            status = 400

        return Response(
            bytes(mvt), content_type="application/vnd.mapbox-vector-tile", status=status
        )


class AOIMVTView(BaseGeodataMVTView):
    model = AOI


class SectorMVTView(BaseGeodataMVTView):
    model = Sector


class BlockMVTView(BaseGeodataMVTView):
    model = Block


class BuildingMVTView(BaseGeodataMVTView):
    model = Building


class ClusteredBuildingMVTView(ClusteredGeodataMVTView):
    model = Building


class RoadMVTView(BaseGeodataMVTView):
    model = Road


class PlotMVTView(BaseGeodataMVTView):
    model = Plot


class GreenspaceMVTView(BaseGeodataMVTView):
    model = Greenspace
