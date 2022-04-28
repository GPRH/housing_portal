# Passport Images

During the [import process](imports.md) a table is generated which links street view images to individual building footprints. When a user selects a building in the portal an image of the building is shown in the building passport if one is available. These images are derived from street view images captured for the purposes of machine learning detections and are also uploaded to Mapillary. In order to display an image in the portal the images must be resized and optimized for web display. The **backend** container mounts an `images` directory (on staging this is at `/mnt/data/images`) and this is where the CSV file is stored.

The [https://github.com/bjohare/wb-gprh-db](https://github.com/bjohare/wb-gprh-db) repo contains an `export-images` utility which exports a csv dump of this table for a particular Area of Interest. This CSV file is then used to process and optimize images for the portal.

## Processing building images.

Building footprint images are stored on `S3`. These images are 2033 pixels square and too large to be used for the web. They need to be scaled and optimized for web use. There is a script located at `backend/apps/geodata/utils/process_images.py` which does this. This script takes two arguments: `City` the city to process images for and `csv` the csv file which contains the list of building images to process (see above). This script can be run using the `backend` docker image as follows:

```bash
docker-compose -f staging.yml run --rm backend \
python apps/geodata/utils/process_images.py $city $csv
```

The `city` argument should match the directory on `S3` which contains the images to be processed. The images will be downloaded to a folder at `/mnt/data/images/[country]/[aoi]` and will be served by nginx (see nginx config at `provision/files/nginx_site.conf` for the webserver configuration).
