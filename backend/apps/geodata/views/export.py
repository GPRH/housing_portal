
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from sendfile import sendfile
from rest_framework.permissions import (
    IsAuthenticated, BasePermission)
from apps.geodata.views.permissions import AOIPermission, DownloadPermission

from apps.geodata.exports.export import Export

EXPORT_DIR = settings.EXPORTS_DIR
METADATA_DIR = str(settings.EXPORTS_METADATA_DIR)


class DatasetDownload(APIView):
    """Download services.
       deprecated in favour of static downloads
       see https://github.com/bjohare/wb-housing-prototype/issues/121
    """

    permission_classes = (IsAuthenticated, DownloadPermission)

    def post(self, request, format=None):
        """
        Export data.
        """
        data = request.data
        dataset = data.get('dataset')
        aoi = data.get('aoi')
        format = data.get('format')
        export = Export(aoi, dataset, format)
        result = export.export_dataset()
        if not result:
            return Response(
                _('No data.'), status=204, content_type="application/json",
            )
        return Response(
            {'download_url': result['zipfile']},
            content_type='application/json',
        )


class RetrieveExport(APIView):

    permission_classes = (IsAuthenticated, AOIPermission)

    def get(self, request, *args, **kwargs):
        country = kwargs.get('country')
        aoi = kwargs.get('aoi')
        filename = kwargs.get('filename')
        path = '{0}{1}/{2}/{3}'.format(EXPORT_DIR, country, aoi, filename)
        return sendfile(
            request, path, attachment=True, attachment_filename=filename,
        )
