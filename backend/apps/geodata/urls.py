from django.urls import path
from django.views.decorators.cache import cache_page
from apps.geodata.views.api import (
    SimpleAOIListAPIView, AOIListAPIView, SectorListAPIView, BlockListAPIView,
    BuildingListAPIView, SectorStatsAPIView, AOIStatsAPIView, AreaStatsAPIView,
    BlockStatsAPIView, RoadListAPIView, PlotListAPIView, GreenspaceListAPIView,
    BuildingRetrieveAPIView, BuildingImageAPIView, SectorLabelListAPIView,
    DroneImageryAPIView, ContactAPIView, ExtraAttrFilterAPIView,
)
from apps.geodata.views.mvt import (
    AOIMVTView, SectorMVTView, BlockMVTView,
    BuildingMVTView, RoadMVTView, PlotMVTView,
    GreenspaceMVTView, ClusteredBuildingMVTView
)
from apps.geodata.views.export import DatasetDownload, RetrieveExport

app_name = 'geodata'

THIRTY_MINS = 60 * 30
ONE_WEEK = 60 * 60 * 24 * 7
ONE_MONTH = THIRTY_MINS * 2 * 24 * 30
ONE_YEAR = ONE_WEEK * 52

urlpatterns = [
    # geojson endpoints
    path('aoinames/', cache_page(ONE_YEAR, key_prefix="aoi-names")
         (SimpleAOIListAPIView.as_view()), name='simple-aoi-list'),

    path('aois/', cache_page(ONE_YEAR, key_prefix='aois')
         (AOIListAPIView.as_view()), name="aoi-list"),

    path('sectors/', cache_page(ONE_YEAR)
         (SectorListAPIView.as_view()), name="sector-list"),

    path('sectorlabels/', cache_page(ONE_YEAR)
         (SectorLabelListAPIView.as_view()), name="sector-label-list"),

    path('blocks/', cache_page(ONE_YEAR)
         (BlockListAPIView.as_view()), name="block-list"),

    path('buildings/', cache_page(ONE_YEAR, key_prefix="buildings")
         (BuildingListAPIView.as_view()), name="building-list"),

    path('buildings/', cache_page(ONE_YEAR, key_prefix="buildings")
         (BuildingListAPIView.as_view()), name="building-list"),

    path('buildings/<int:id>/', cache_page(ONE_YEAR,
                                           key_prefix="building-detail")
         (BuildingRetrieveAPIView.as_view()),
         name="building-detail"),

    path('roads/', cache_page(ONE_YEAR, key_prefix="roads")
         (RoadListAPIView.as_view()), name="road-list"),

    path('plots/', cache_page(ONE_YEAR, key_prefix="plots")
         (PlotListAPIView.as_view()), name="plot-list"),

    path('greenspaces/', cache_page(ONE_YEAR, key_prefix="greenspace")
         (GreenspaceListAPIView.as_view()), name="greenspace-list"),

    path('blockstats/', BlockStatsAPIView.as_view(), name="block-stats"),

    path('sectorstats/', cache_page(ONE_YEAR, key_prefix='sector-stats')
         (SectorStatsAPIView.as_view()), name="sector-stats"),

    path('aoistats/', cache_page(ONE_YEAR, key_prefix="aoi-stats")
         (AOIStatsAPIView.as_view()), name="aoi-stats"),

    path('areastats/', AreaStatsAPIView.as_view(), name="area-stats"),

    path('building-attributes/<str:aoi>/<str:key>/<str:value>',
         ExtraAttrFilterAPIView.as_view(),
         name='extra-attrs-filter'),

    # export endpoints
    # path('download/', DatasetDownload.as_view(), name="download"),
    path('exports/<str:country>/<str:aoi>/<str:filename>',
         RetrieveExport.as_view(), name="exports"),

    # images
    path('images/<str:country>/<str:aoi>/<str:image>',
         cache_page(ONE_YEAR, key_prefix="images")
         (BuildingImageAPIView.as_view()), name="building-image"),

    # drone imagery xyz endpoint
    path('drone/<str:aoi>/<int:z>/<int:x>/<int:y>.png',
         cache_page(ONE_YEAR, key_prefix="drone")
         (DroneImageryAPIView.as_view()), name='drone-imagery'),

    # contact endpoint
    path('contact/', ContactAPIView.as_view(), name='contact'),


    # MVT endpoints
    path("aoi/<int:aoi_id>/.mvt/", cache_page(
        ONE_YEAR, key_prefix='mvt-aoi')
        (AOIMVTView.as_view()), name='aoi-mvt'),

    path("sectors/<int:aoi_id>/.mvt/", cache_page(
        ONE_YEAR, key_prefix="mvt-sector")
        (SectorMVTView.as_view()), name="sector-mvt"),

    path("blocks/<int:aoi_id>/.mvt/", cache_page(
        ONE_YEAR, key_prefix="mvt-block")
        (BlockMVTView.as_view()), name="block-mvt"),

    path("buildings/<int:aoi_id>/.mvt/", cache_page(
        ONE_YEAR, key_prefix="mvt-building")
        (BuildingMVTView.as_view()), name="building-mvt"),

    path("clustered-buildings/<int:aoi_id>/.mvt/",
         ClusteredBuildingMVTView.as_view(), name="clustered-building-mvt"),

    path("plots/<int:aoi_id>/.mvt/", cache_page(
        ONE_YEAR, key_prefix="mvt-plot")
        (PlotMVTView.as_view()), name="plot-mvt"),

    path("roads/<int:aoi_id>/.mvt/", cache_page(
        ONE_YEAR, key_prefix="mvt-road")
        (RoadMVTView.as_view()), name="road-mvt"),

    path("greenspace/<int:aoi_id>/.mvt/", cache_page(
        ONE_YEAR, key_prefix="mvt-greenspace")
        (GreenspaceMVTView.as_view()), name="greenspace-mvt"),
]
