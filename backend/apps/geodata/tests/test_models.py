import pytest
from django.test import TestCase
from apps.geodata.models import Building


class BuildingTotalQualityTest(TestCase):
    fixtures = [
        'apps/geodata/tests/fixtures/quality.json',
    ]

    # @pytest.mark.skip
    def test_very_good(self):
        bu = Building.objects.get(id=4247)
        bu.save()
        bu.refresh_from_db()
        assert bu.tot_qualit == 'very good'

    # @pytest.mark.skip
    def test_d_cond_good_sv_condit_other(self):
        bu = Building.objects.get(id=4250)
        bu.save()
        bu.refresh_from_db()
        assert bu.tot_qualit == 'good'

    # @pytest.mark.skip
    def test_d_cond_other_sv_condit_good(self):
        bu = Building.objects.get(id=4251)
        bu.save()
        bu.refresh_from_db()
        assert bu.tot_qualit == 'good'

    # @pytest.mark.skip
    def test_d_cond_fair_sv_condit_fair(self):
        bu = Building.objects.get(id=4252)
        bu.save()
        bu.refresh_from_db()
        assert bu.tot_qualit == 'fair'

    # @pytest.mark.skip
    def test_d_cond_good_sv_condit_fair(self):
        bu = Building.objects.get(id=4253)
        bu.save()
        bu.refresh_from_db()
        assert bu.tot_qualit == 'fair'

    # @pytest.mark.skip
    def test_d_cond_fair_sv_condit_good(self):
        bu = Building.objects.get(id=4254)
        bu.save()
        bu.refresh_from_db()
        assert bu.tot_qualit == 'fair'

    # @pytest.mark.skip
    def test_d_cond_fair_sv_condit_other(self):
        bu = Building.objects.get(id=4255)
        bu.save()
        bu.refresh_from_db()
        assert bu.tot_qualit == 'fair'

    # @pytest.mark.skip
    def test_d_cond_other_sv_condit_fair(self):
        bu = Building.objects.get(id=4256)
        bu.save()
        bu.refresh_from_db()
        assert bu.tot_qualit == 'fair'

    # @pytest.mark.skip
    def test_d_cond_poor_sv_condit_good_fair_other(self):
        bu = Building.objects.get(id=4257)
        bu.save()
        bu.refresh_from_db()
        assert bu.tot_qualit == 'poor'

    # @pytest.mark.skip
    def test_d_cond_good_fair_other_sv_condit_poor(self):
        bu = Building.objects.get(id=4258)
        bu.save()
        bu.refresh_from_db()
        assert bu.tot_qualit == 'poor'

    # @pytest.mark.skip
    def test_d_cond_poor_sv_condit_poor(self):
        bu = Building.objects.get(id=4259)
        bu.save()
        bu.refresh_from_db()
        assert bu.tot_qualit == 'very poor'

    def test_catch_default(self):
        bu = Building.objects.get(id=4260)
        bu.save()
        bu.refresh_from_db()
        assert bu.tot_qualit == None
