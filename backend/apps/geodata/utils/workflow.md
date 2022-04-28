# Raster tile generation workflow.

Can use the backend docker instance to run these commands as the necessary gdal tools are installed.

## Merge raster files

```
gdalbuildvrt merged.vrt *.tif
```

## Compress merged TIF file.

```
gdal_translate -co COMPRESS=LZW -co TILED=YES -co BIGTIFF=YES merged.tif pozon_tiled.tif
```

## Reproject the TIF.

```
 gdalwarp -of GTiff -co TILED=YES -co COMPRESS=LZW -co BIGTIFF=YES -s_srs EPSG:32618 -t_srs EPSG:3857 pozon_tiled.tif pozon_tiled_web.tif

```

## Generate XYZ tiles.

Zoom levels between 14 - 21.

```
./gdal2tilesp.py -z '14-21' pozon_tiled_web.tif
```
