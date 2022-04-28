import os
import boto3
import csv
import environ
import logging
import argparse
from PIL import Image
from pathlib import Path

env = environ.Env()
logging.basicConfig(
    filename='/images/process_images.log',
    format='%(levelname)s:%(message)s',
    level=logging.INFO,
)

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')
BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

S3_IMAGE_ROOT = env('S3_IMAGE_ROOT')
IMG_DIR = env('IMAGE_DIR')
COUNTRY = env('PORTAL_INSTANCE')
SIZE = (350, 350)


def process_images(city, image_dir, csv_file_path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            path = _get_image_path(city, row)
            _process_image(image_dir, path)


def _get_image_path(city, row):
    subfolder = row['subfolder']
    frame = row['frame']
    cam = row['cam']
    path = '{0}{1}/{2}/{3}_Cam{4}.jpg'.format(
        S3_IMAGE_ROOT, city, subfolder, frame, cam)
    return path


def _process_image(image_dir, path):
    parts = path.split('/')
    filename = '{0}_{1}'.format(parts[3], parts[4])
    file_path = '{0}/{1}'.format(image_dir, filename)
    if Path(file_path).is_file():
        logging.info("Founding existing image at: %s", file_path)
        return
    s3 = boto3.client(
        's3', aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    try:
        with open(file_path, 'wb') as f:
            s3.download_fileobj(BUCKET_NAME, path, f)
        img = Image.open(file_path)
        img = img.resize(SIZE, Image.ANTIALIAS)
        img.save(
            file_path, "JPEG", optimize=True, progressive=True,
        )
        logging.info("Processed: %s", path)
    except Exception as e:
        logging.warning("%s : %s", e, path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Process GPRH streetview images.')
    parser.add_argument(
        'city', metavar='City', type=str,
        help='the city to process',
    )
    parser.add_argument(
        'csv', metavar='Csv', type=str,
        help='the csv file to process'
    )
    args = parser.parse_args()
    city = args.city
    csv_file = args.csv
    image_dir = "{0}{1}/{2}".format(IMG_DIR,
                                    COUNTRY.lower(), city.lower())
    csv_file_path = "{0}{1}".format(IMG_DIR, csv_file)
    logging.info("Image directory is: %s", image_dir)
    if not os.path.exists(image_dir):
        os.makedirs(image_dir, exist_ok=True)
    process_images(city.upper(), image_dir, csv_file_path)
