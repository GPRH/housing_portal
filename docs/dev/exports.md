# Exporting data

Exports for an Area of Interest (for example 'El Pozon') can be created by running the following script from the root of the portal source directory:

```
./exportdata 'El Pozon'
```

This script's output will look like:

```
Starting at: 2020-10-06 11:41:46.201883
{'zipfile': '/exports/colombia/el-pozon/el-pozon-sectors-gpkg.zip'}
{'zipfile': '/exports/colombia/el-pozon/el-pozon-sectors-csv.zip'}
{'zipfile': '/exports/colombia/el-pozon/el-pozon-sectors-geojson.zip'}
...
{'zipfile': '/exports/colombia/el-pozon/el-pozon-sectors-shp.zip'}
{'zipfile': '/exports/colombia/el-pozon/el-pozon-buildings-gpkg.zip'}
{'zipfile': '/exports/colombia/el-pozon/el-pozon-buildings-csv.zip'}
{'zipfile': '/exports/colombia/el-pozon/el-pozon-greenspace-shp.zip'}
Ending at: 2020-10-06 11:43:10.482873
Export took: 0:01:24.280990
```

Currently, this script exports `buidlings`, `sectors` and `greenspaces` as `geojson`, `geopackage`, `shapefile` and `csv`.

Exports are stored to the `exports` docker volume in a directory named for the portal instance country.

These files can be downloaded from the frontend using the `Data Download` tool which is available from the user menu.
