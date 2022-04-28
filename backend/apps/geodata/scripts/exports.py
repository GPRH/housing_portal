from apps.geodata.exports.export import Export
from apps.geodata.models import AOI
import concurrent.futures
from django import db
from datetime import datetime


def run_export(data):
    db.connection.close()
    aoi, dataset, fmt = data
    exp = Export(aoi, dataset, fmt)
    result = exp.export_dataset()
    return result


def run(*args):
    if (len(args) != 1):
        print('Please provide the AOI name to export.')
    try:
        AOI.objects.get(name=args[0])
    except AOI.DoesNotExist:
        print(f"AOI '{args[0]}' not found.")
        exit()
    aoi = str(args[0])
    data = []
    for dataset in ['sectors', 'buildings', 'greenspace']:
        for fmt in ['gpkg', 'csv', 'geojson', 'shp']:
            data.append((aoi, dataset, fmt))
    start = datetime.now()
    print('Starting at: {0}'.format(start))
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for d in data:
            result = executor.submit(run_export, d)
            print(result.result())
    end = datetime.now()
    print('Ending at: {0}'.format(end))
    print('Export took: {0}'.format(end - start))
