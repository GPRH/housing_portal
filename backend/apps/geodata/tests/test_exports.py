import json
import os
import pytest
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.shortcuts import reverse
from apps.users.tests.factories import UserFactory
from django.contrib.auth.models import Group
from apps.geodata.tests.utils import clear_temp, clear_exports
from apps.geodata.exports.export import Export


@pytest.mark.skip
@pytest.mark.usefixtures('clear_temp')
class DownloadDatasetAPITest(APITestCase):

    fixtures = [
        'apps/geodata/tests/fixtures/pozon.json',
        'apps/geodata/tests/fixtures/soledad.json',
        'apps/geodata/tests/fixtures/perms.json',
        'apps/geodata/tests/fixtures/groups.json',
    ]

    def setUp(self):
        self.client = APIClient()

    def tearDown(self):
        self.client.logout()

    def test_get_with_anonymous_user(self):
        response = self.client.get(reverse('geodata:download'))
        assert response.status_code == 403

    def test_get_with_authenticated_user(self):
        user = UserFactory.create(
            email='test@test.com', password='secret',
        )
        group = Group.objects.get(name='TestColombiaAdminUserGroup')
        user.groups.add(group)
        self.client.login(email='test@test.com', password='secret')
        response = self.client.get(reverse('geodata:download'))
        assert response.status_code == 405  # method not allowed

    def test_get_aggregated_sector_stats(self):
        user = UserFactory.create(
            email='test@test.com', password='secret',
        )
        group = Group.objects.get(name='TestColombiaAdminUserGroup')
        user.groups.add(group)
        self.client.login(email='test@test.com', password='secret')
        response = self.client.post(
            reverse('geodata:download'),
            {'aoi': 'El Pozon', 'dataset': 'sectors', 'format': 'csv'})
        assert response.status_code == 200
        content = json.loads(response.content)
        assert 'download_url' in content.keys()


@pytest.mark.usefixtures('clear_exports')
class ExportTest(TestCase):

    fixtures = [
        'apps/geodata/tests/fixtures/pozon.json',
        'apps/geodata/tests/fixtures/soledad.json',
        'apps/geodata/tests/fixtures/perms.json',
        'apps/geodata/tests/fixtures/groups.json',
    ]

    def test_csv_exports(self):
        aoi = 'El Pozon'
        dataset = 'sectors'
        format = 'csv'
        export = Export(aoi, dataset, format)
        result = export.export_dataset()
        assert result is not None
        assert os.path.exists(result['zipfile'])
        assert 'csv' and 'sectors' in result['zipfile']

    def test_shp_sector_exports(self):
        aoi = 'El Pozon'
        dataset = 'sectors'
        format = 'shp'
        export = Export(aoi, dataset, format)
        result = export.export_dataset()
        assert result is not None
        assert os.path.exists(result['zipfile'])
        assert 'shp' and 'sectors' in result['zipfile']

    def test_gpkg_exports(self):
        aoi = 'La Central'
        dataset = 'buildings'
        format = 'gpkg'
        export = Export(aoi, dataset, format)
        result = export.export_dataset()
        assert result is not None
        assert os.path.exists(result['zipfile'])
        assert 'gpkg' and 'buildings' in result['zipfile']

    def test_shp_exports(self):
        aoi = 'La Central'
        dataset = 'buildings'
        format = 'shp'
        export = Export(aoi, dataset, format)
        result = export.export_dataset()
        assert result is not None
        assert os.path.exists(result['zipfile'])
        assert 'shp' and 'buildings' in result['zipfile']

    def test_geojson_exports(self):
        aoi = 'La Central'
        dataset = 'buildings'
        format = 'geojson'
        export = Export(aoi, dataset, format)
        result = export.export_dataset()
        assert result is not None
        assert os.path.exists(result['zipfile'])
        assert 'geojson' and 'buildings' in result['zipfile']

    def test_nodata_exports(self):
        aoi = 'El Pozon'
        dataset = 'buildings'
        format = 'gpkg'
        export = Export(aoi, dataset, format)
        result = export.export_dataset()
        assert result is None
