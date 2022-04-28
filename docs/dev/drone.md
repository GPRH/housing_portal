# Aerial Imagery

This is a general overview of the approach to prepartion of aerial imagery for the portal, adjustments may need to be made depending on the particular charcteristics of the input raster dataset. Best practice is to output all intermediate steps as gdal `VRT`, see [https://gdal.org/drivers/raster/vrt.html](https://gdal.org/drivers/raster/vrt.html) for more details.

The ansible deployment scripts install `gdal` on the host staging or production machine which makes the preparation of the drone imagery possible.

On production / staging envrionents the `backend` docker container should mount a directory at `/drone`. This directory would ideally be some kind of block storage device (eg Digital Ocean or AWS Volume). The staging / production config should be updated to reflect the mount point. The `/drone` directory should have the following structure:

- `/drone/files/{aoi}`: contains raw tif files for processing into tile pyramids. Sub-directories are named for each area of interest.
- `/drone/{aoi}`: where the tilesets should be stored by area of interest.

This directory is exposed by nginx for delivery of drone imagery layers. See the nginx configuration at `provision/files/nginx_site.comf`.

## Merge raster files

On the staging / production machine, change to the requred directory, eg `/mnt/data/drone/files/el-pozon`. To build a VRT mosaic of the .tif files run:

```bash
gdalbuildvrt mosaic.vrt *.tif
```

or if an alphaband is missing in the source tiffs.

```bash
gdalbuildvrt -addalpha mosaic.vrt *.tif
```

## Reproject the VRT

Running `gdalinfo` against a sample of the input rasters will show the current projection.

```bash
gdalinfo some_input_raster.tif
```

Reproject the rasters.

```bash
 gdalwarp -of VRT -co COMPRESS=JPEG -co TILED=YES \
 -s_srs EPSG:{{ existing_code }} -t_srs EPSG:3857 mosaic.vrt output.vrt
```

The `output.vrt` can now be used to generate the tiles.

## Generate XYZ tiles

A copy of `gdal2tiles.py` which supports multiprocessing is installed by the deployment process. This is installed at `/mnt/data/drone/files/gdal2tiles.py`.

Typically, the portal requires tiles from Zoom levels 14 - 21. To generate the tiles from the `/mnt/data/drone/files/el-pozon` directory, run:

```bash
nohup ./gdal2tilesp.py --w leaflet --xyz --processes=4 \
-v z '14-21' el-pozon/output.vrt ../el-pozon &
```

This will generate a tile pyramid in xyz format with a leaflet.html web viewer page. Running `tail -f nohup.out` will track the output. See the [gdal2tiles](https://gdal.org/programs/gdal2tiles.html) page of the GDAL docs for more information.
