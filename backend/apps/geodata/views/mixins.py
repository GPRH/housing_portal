import pandas as pd
import json
import math
from django.conf import settings
from django.db.models.functions import Lower, Replace
from django.db.models import Sum, Min, Max, Avg, Value, Q
from apps.geodata.models import (
    AOI, Building, Road, Greenspace
)
from django.contrib.gis.db.models.functions import (
    Length, Transform, Area, Intersection, Centroid,
)


class AOIQuerysetMixin:
    def get_queryset(self):
        # filter queryset based on user permissions
        queryset = AOI.objects.all()
        user = self.request.user
        groups = user.groups.all()
        perms = []
        for group in groups:
            perms = perms + [
                perm.codename.split('_')[1]
                for perm in group.permissions.all()
            ]
        perms = list(set(perms))
        return queryset.annotate(
            cl=Lower(Replace('city', Value(' '), Value('')))).filter(
                cl__in=perms).order_by('city', 'name')


class RelatedAOIFilterMixin:

    def _get_filtered_queryset(self, queryset):
        # filter queryset based on user permissions
        user = self.request.user
        groups = user.groups.all()
        perms = []
        for group in groups:
            perms = perms + [
                perm.codename.split('_')[1]
                for perm in group.permissions.all()
            ]
        return queryset.annotate(
            cl=Lower(Replace('aoi__city', Value(' '), Value('')))).filter(
                cl__in=perms).order_by('aoi__city', 'aoi__name')


class StatsMixin:

    def get_epsg(self):
        return settings.LOCAL_EPSG

    def _building_stats(self, obj=None, geom=None):
        stats = dict()
        if not obj and geom:
            buildings = Building.objects.annotate(
                centroid=Centroid('geom')).filter(
                centroid__within=geom).annotate(
                    geom_local=Transform('geom', self.get_epsg()))
        else:
            buildings = obj.buildings.annotate(
                geom_local=Transform('geom', self.get_epsg()))
        count = buildings.count()

        count_tot_quality = buildings.exclude(tot_qualit__isnull=True).count()
        v_good = buildings.filter(tot_qualit='very good').count()
        good = buildings.filter(tot_qualit='good').count()
        fair = buildings.filter(tot_qualit='fair').count()
        poor = buildings.filter(tot_qualit='poor').count()
        v_poor = buildings.filter(tot_qualit='very poor').count()

        pvp = round(v_poor / count_tot_quality * 100, 2) if v_poor else 0
        pp = round(poor / count_tot_quality * 100, 2) if poor else 0
        pf = round(fair / count_tot_quality * 100, 2) if fair else 0
        pg = round(good / count_tot_quality * 100, 2) if good else 0
        pvg = round(v_good / count_tot_quality * 100, 2) if v_poor else 0

        # building stats
        buildings = buildings.annotate(area=Area('geom_local'))
        building_ids = buildings.values_list('id', flat=True)
        size = buildings.aggregate(
            total_area=Sum(Area('geom_local')))['total_area']
        height = buildings.aggregate(
            total_height=Sum('d_avg_height'))['total_height']
        size_bins = self._get_building_size_bins(buildings)
        building_size = buildings.aggregate(
            min_size=Min('area'), max_size=Max('area'))
        min_size = building_size['min_size']
        max_size = building_size['max_size']
        if (min_size is not None and max_size is not None):
            min_size = round(min_size.sq_m, 2)
            max_size = round(max_size.sq_m, 2)
        building_height = buildings.aggregate(
            min_height=Min('d_avg_height'), max_height=Max('d_avg_height'))
        height_bins = self._get_building_height_bins(buildings)
        min_height = building_height['min_height']
        max_height = building_height['max_height']
        if (min_height is not None and max_height is not None):
            min_height = round(building_height['min_height'], 2)
            max_height = round(building_height['max_height'], 2)
        size = buildings.aggregate(
            total_area=Sum(Area('geom_local')))['total_area']
        height = buildings.aggregate(
            total_height=Sum('d_avg_height'))['total_height']

        # taxes
        tax_stats = buildings.aggregate(
            total_taxes=Sum('pt_sum'),
            total_taxes_owed=Sum('pt_sum_owed'),
            total_tax_count=Sum('count')
        )
        if tax_stats['total_tax_count'] == 0:
            tax_bins = []
            tax_owed_bins = []
        else:
            tax_bins = self._get_tax_bins(buildings)
            tax_owed_bins = self._get_tax_owed_bins(buildings)
        tax_min_max = buildings.aggregate(
            min_tax=Min('pt_avg'), max_tax=Max('pt_avg'),
            min_tax_owed=Min('pt_avg_owed'), max_tax_owed=Max('pt_avg_owed')
        )
        min_tax = tax_min_max['min_tax']
        max_tax = tax_min_max['max_tax']
        min_tax_owed = tax_min_max['min_tax_owed']
        max_tax_owed = tax_min_max['max_tax_owed']

        res = buildings.filter(sv_use='residential').count()
        # comm = buildings.filter(
        #     Q(sv_use='non_residential') | Q(
        #         sv_use='critical_infrastructure')
        # ).count()
        comm = buildings.filter(sv_use='non_residential').count()
        critical = buildings.filter(sv_use='critical_infrastructure').count()
        mixed = buildings.filter(sv_use='mixed').count()
        unknown = buildings.filter(sv_use="").count()
        public = buildings.filter(land_publi=1).count()
        resettle = buildings.filter(dem_reset='yes').count()
        softstory = buildings.filter(soft_story='yes').count()

        pres = round(res / count * 100, 2) if res else 0
        pcomm = round(comm / count * 100, 2) if comm else 0
        pmixed = round(mixed / count * 100, 2) if mixed else 0
        pcritical = round(critical / count * 100, 2) if critical else 0
        punknown = round(unknown / count * 100, 2) if unknown else 0
        ppublic = round(public / count * 100, 2) if public else 0
        presettle = round(resettle / count * 100, 2) if resettle else 0
        psoftstory = round(softstory / count * 100, 2) if softstory else 0

        stats['building_ids'] = building_ids
        stats['count'] = count
        stats['very_poor'] = pvp
        stats['poor'] = pp
        stats['fair'] = pf
        stats['good'] = pg

        #  percentage tot_quality
        stats['very_good'] = pvg
        stats['very_poor_count'] = v_poor
        stats['poor_count'] = poor
        stats['fair_count'] = fair
        stats['good_count'] = good
        stats['very_good_count'] = v_good

        stats['resettle'] = resettle
        stats['per_resettle'] = presettle
        stats['softstory'] = softstory
        stats['per_softstory'] = psoftstory

        stats['size_bins'] = size_bins
        stats['min_size'] = min_size
        stats['max_size'] = max_size
        stats['height_bins'] = height_bins
        stats['min_height'] = min_height
        stats['max_height'] = max_height
        stats['avg_size'] = round(
            size.sq_m / count, 2) if size and count else 0
        stats['avg_height'] = round(
            height / count, 2) if height and count else 0
        stats['residential'] = round(
            res / count * 100, 2) if res and count else 0
        stats['commercial'] = round(
            comm / count * 100, 2) if comm and count else 0
        stats['critial'] = round(
            critical / count * 100, 2) if critical and count else 0
        stats['mixed'] = round(mixed / count * 100,
                               2) if mixed and count else 0
        stats['unknown'] = round(unknown / count * 100,
                                 2) if unknown and count else 0
        stats["public_count"] = public
        stats['per_public'] = ppublic
        stats['residential_count'] = res
        stats['per_residential'] = pres
        stats['commercial_count'] = comm
        stats['per_commercial'] = pcomm
        stats['mixed_count'] = mixed
        stats['per_mixed'] = pmixed
        stats['critical_count'] = critical
        stats['per_critical'] = pcritical
        stats['unknown_count'] = unknown
        stats['per_unknown'] = punknown
        stats['min_tax'] = min_tax
        stats['max_tax'] = max_tax
        stats['min_tax_owed'] = min_tax_owed
        stats['max_tax_owed'] = max_tax_owed
        stats['taxes'] = {
            'total_taxes': tax_stats['total_taxes'],
            'total_taxes_owed': tax_stats['total_taxes_owed'],
            'total_tax_records': tax_stats['total_tax_count'],
            'tax_bins': tax_bins, 'tax_owed_bins': tax_owed_bins
        }
        return stats

    def _get_building_size_bins(self, buildings):
        if buildings.count() == 0:
            return []
        areas = [x for x in buildings.values_list('d_area', flat=True)]
        if not any(areas):
            return []
        area_df = pd.DataFrame(pd.qcut(areas, 8, duplicates='drop'))
        categories = [
            math.floor(x['right'])
            for x in json.loads(area_df[0].to_json()).values()
        ]
        bins = list(set(categories))
        bins.insert(0, 0)
        bins.sort()
        return bins

    def _get_building_height_bins(self, buildings):
        if buildings.count() == 0:
            return []
        heights = [x for x in buildings.values_list('d_avg_height', flat=True)]
        if not any(heights):
            return []
        height_df = pd.DataFrame(pd.qcut(heights, 5, duplicates='drop'))
        categories = [
            math.floor(x['right'])
            for x in json.loads(height_df[0].to_json()).values()
        ]
        bins = list(set(categories))
        bins.insert(0, 0)
        bins.sort()
        return bins

    def _get_tax_bins(self, buildings):
        if buildings.count() == 0:
            return []
        averages = [x for x in buildings.values_list('pt_avg', flat=True)]
        avg_df = pd.DataFrame(pd.qcut(averages, 12, duplicates='drop'))
        categories = [
            math.floor(x['right'])
            for x in json.loads(avg_df[0].to_json()).values()
        ]
        bins = list(set(categories))
        bins.insert(0, 0)
        bins.sort()
        return bins

    def _get_tax_owed_bins(self, buildings):
        if buildings.count() == 0:
            return []
        averages = [x for x in buildings.values_list('pt_avg_owed', flat=True)]
        avg_df = pd.DataFrame(pd.qcut(averages, 12, duplicates='drop'))
        categories = [
            math.floor(x['right'])
            for x in json.loads(avg_df[0].to_json()).values()
        ]
        bins = list(set(categories))
        bins.insert(0, 0)
        bins.sort()
        return bins

    def _greenspace_stats(self, obj=None, geom=None):
        stats = dict()
        if not obj and geom:
            geom_local = geom.transform(
                self.get_epsg(), clone=True)
            greenspaces = Greenspace.objects.filter(
                geom__intersects=geom).annotate(
                geom_local=Transform('geom', self.get_epsg()))
        else:
            geom_local = obj.geom_local
            greenspaces = Greenspace.objects.annotate(
                geom_local=Transform('geom', self.get_epsg()))

        gs = greenspaces.filter(
            geom_local__intersects=geom_local).annotate(
            intersection=Intersection('geom_local', geom_local),
        )
        intersection = gs.aggregate(
            total_intersection=Sum(Area('intersection')))
        tot_gs = intersection['total_intersection']
        stats['total_area'] = round(tot_gs.sq_m, 2) if tot_gs else 0
        stats['per_sec_area'] = round(
            tot_gs.sq_m / geom_local.area * 100, 2) if tot_gs else 0
        return stats

    def _road_stats(self, obj):
        stats = dict()
        roads = Road.objects.annotate(
            geom_local=Transform('geom', self.get_epsg()),
        )
        rs = roads.filter(
            geom_local__intersects=obj.geom_local,
        ).annotate(intersection=Intersection(
            'geom_local', obj.geom_local)
        )
        paved = rs.filter(surface='paved').aggregate(
            total_length=Sum(Length('intersection')),
        )
        unpaved = rs.filter(surface='unpaved').aggregate(
            total_length=Sum(Length('intersection')),
        )
        paved_length = paved['total_length']
        unpaved_length = unpaved['total_length']
        stats['paved_length'] = round(
            paved_length.m / 1000, 2) if paved_length else 0
        stats['unpaved_length'] = round(
            unpaved_length.m / 1000, 2) if unpaved_length else 0
        return stats

    def _k3_stats(self, obj):
        blocks = obj.blocks.filter(k3__isnull=False)
        k3 = blocks.aggregate(
            avg_k3=Avg('k3'), min_k3=Min('k3'), max_k3=Max('k3')
        )
        return k3
