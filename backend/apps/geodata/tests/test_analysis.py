from django.test import TestCase
from apps.geodata.models import AOI, Sector, Building


class SectorTestCase(TestCase):

    fixtures = ['apps/geodata/tests/fixtures/pozon.json']

    def setUp(self):
        self.aoi = AOI.objects.first()
        self.sector = Sector.objects.first()

    def test_fixture_loading(self):
        assert AOI.objects.count() == 1
        assert Sector.objects.count() == 2
        assert Building.objects.count() == 6

        assert self.aoi.sectors.count() == 2
        assert self.aoi.buildings.count() == 6
        assert self.sector.buildings.count() == 6

    def test_analysis_attrs(self):
        assert self.sector.buildings.filter(tot_qualit='poor').count() == 2
        assert self.sector.buildings.filter(soft_story='YES').count() == 0
        assert self.sector.buildings.filter(dem_reset='NO').count() == 6
        assert Building.objects.filter(dem_struct='NO').count() == 6
