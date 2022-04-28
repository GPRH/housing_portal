# To insert building ids into prepared buildings file

Using the devseed postgis dump:

1. Update the srid on the buildings footprint:

```
SELECT UpdateGeometrySRID('buildings', 'footprint', 4326);
```

2. Import the prepared buildings file into the postgis db. This can be done using QGIS or ogr on the command line.

3. Once imorted run the following sql to create a new table with the original building_id:

```
select * into brena_buildings_notax_building_id from (select b.id as building_id, bb.* from buildings b, brena_building_notax bb where st_within(st_centroid(b.footprint), bb.geom)) as temp;
```

4. Export this to a shapefile and use for portal imports.
